#!/usr/bin/env python3
"""
Group similar photos into numbered folders.

- Walks an input directory recursively and reads images.
- Extracts features using MediaPipe Pose (if available) to group same/near-same poses.
- Falls back to perceptual hash (pHash) for visual similarity if pose isn't available.
- Clusters images and copies/moves them into output folders named 1, 2, 3, ...

Requirements:
- Pillow
- imagehash
- numpy
- scikit-learn
- optional: mediapipe (for better pose-based grouping)
"""

import argparse
import os
import sys
import shutil
from pathlib import Path
from typing import List, Tuple, Optional, Dict

import numpy as np
from PIL import Image, UnidentifiedImageError
import imagehash

MP_SOLUTIONS = None
try:
    import mediapipe as mp  # type: ignore
    try:
        # Newer installs typically expose mp.solutions
        MP_SOLUTIONS = mp.solutions  # type: ignore[attr-defined]
    except AttributeError:
        # Some builds expose solutions under mediapipe.python.solutions
        from mediapipe.python import solutions as MP_SOLUTIONS  # type: ignore
    HAS_MEDIAPIPE = MP_SOLUTIONS is not None
except Exception:
    HAS_MEDIAPIPE = False

from sklearn.cluster import DBSCAN

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def find_images(root: Path, exclude: Optional[Path] = None) -> List[Path]:
    images: List[Path] = []
    root = root.resolve()
    excl = exclude.resolve() if exclude else None
    for p in root.rglob("*"):
        try:
            if excl and p.resolve().is_relative_to(excl):
                continue
        except AttributeError:
            # Fallback for Python < 3.9
            if excl and str(p.resolve()).startswith(str(excl)):
                continue
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            images.append(p)
    return images


def load_image(path: Path) -> Optional[Image.Image]:
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        return img
    except (UnidentifiedImageError, OSError):
        return None


# ------------------ Pose feature extraction ------------------

def extract_pose_features(img: Image.Image) -> Optional[np.ndarray]:
    if not HAS_MEDIAPIPE or MP_SOLUTIONS is None:
        return None
    try:
        # MediaPipe expects numpy arrays in RGB
        arr = np.array(img)
        mp_pose = MP_SOLUTIONS.pose  # type: ignore[attr-defined]
        # static_image_mode=True since we're not in a video stream
        with mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False) as pose:
            res = pose.process(arr)
            if not res.pose_landmarks:
                return None
            # 33 landmarks; use x,y (normalized by image width/height already in [0,1])
            xs = []
            ys = []
            for lm in res.pose_landmarks.landmark:
                xs.append(lm.x)
                ys.append(lm.y)
            pts = np.stack([np.array(xs), np.array(ys)], axis=1)  # (33,2)
            # Normalize: center and scale for rough scale invariance
            center = pts.mean(axis=0)
            pts_centered = pts - center
            scale = np.median(np.linalg.norm(pts_centered, axis=1))
            if scale <= 1e-6:
                scale = 1.0
            pts_norm = pts_centered / scale
            # Flatten to vector (66,)
            vec = pts_norm.reshape(-1)
            return vec.astype(np.float32)
    except Exception:
        # Any MediaPipe runtime/import issues: treat as unavailable
        return None


# ------------------ pHash feature extraction ------------------

def phash_vector(img: Image.Image) -> np.ndarray:
    h = imagehash.phash(img)  # 64-bit (8x8)
    # h.hash is a numpy array of shape (8,8) with booleans
    bits = np.array(h.hash, dtype=np.uint8).reshape(-1)  # values 0/1
    return bits.astype(np.float32)


# ------------------ Clustering helpers ------------------

def cluster_features(
    features: List[np.ndarray],
    metric: str,
    eps: float,
    min_samples: int,
) -> np.ndarray:
    if not features:
        return np.array([])
    X = np.stack(features, axis=0)
    # DBSCAN: metric can be 'euclidean' for pose, 'hamming' for bit vectors
    model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    labels = model.fit_predict(X)
    return labels  # -1 for noise


# ------------------ Grouping logic ------------------

def group_and_copy(
    image_paths: List[Path],
    labels: np.ndarray,
    out_dir: Path,
    move: bool,
    start_index: int = 1,
    input_dir: Optional[Path] = None,
) -> int:
    """Copy/move images into folders 1,2,3,... according to labels.
    Preserves one level of source subfolder structure if present.
    Returns last used folder index + 1 for chaining.
    """
    if len(image_paths) == 0:
        return start_index
    # Build clusters: label -> list of paths
    clusters: Dict[int, List[Path]] = {}
    for p, lab in zip(image_paths, labels):
        clusters.setdefault(int(lab), []).append(p)

    # Assign only clusters with non-negative labels a folder
    cur = start_index
    for lab, paths in sorted(clusters.items(), key=lambda kv: kv[0]):
        if lab < 0:
            continue  # skip noise cluster
        target = out_dir / str(cur)
        target.mkdir(parents=True, exist_ok=True)
        for src in paths:
            # Determine if image is in a subfolder or at root
            if input_dir and src.parent == input_dir:
                # Image is directly in the input root, no subfolder
                dst = target / src.name
            elif input_dir and src.parent.parent == input_dir:
                # Image is exactly one level deep, preserve folder name
                subfolder = target / src.parent.name
                subfolder.mkdir(parents=True, exist_ok=True)
                dst = subfolder / src.name
            else:
                # Fallback: just use the immediate parent folder name
                subfolder = target / src.parent.name
                subfolder.mkdir(parents=True, exist_ok=True)
                dst = subfolder / src.name
            try:
                if move:
                    shutil.move(str(src), str(dst))
                else:
                    shutil.copy2(str(src), str(dst))
            except Exception as e:
                print(f"[WARN] Failed to {'move' if move else 'copy'} {src}: {e}")
        cur += 1
    return cur


def main():
    parser = argparse.ArgumentParser(description="Group similar photos into numbered folders")
    parser.add_argument("input_dir", type=str, help="Input directory containing images (recursively)")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory to write grouped folders. If not provided, uses current working directory with --task-name, else defaults to <input_dir>/grouped_photos.",
    )
    parser.add_argument(
        "--task-name",
        type=str,
        default=None,
        help="Name for the grouping task; used as folder name when no --output-dir is provided.",
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["auto", "pose", "phash"],
        default="auto",
        help="Feature method: pose (MediaPipe), phash (perceptual hash), or auto fallback",
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying",
    )
    parser.add_argument(
        "--min-cluster-size",
        type=int,
        default=2,
        help="Minimum images per cluster (DBSCAN min_samples)",
    )
    parser.add_argument(
        "--pose-eps",
        type=float,
        default=0.2,
        help="DBSCAN eps for pose features (euclidean distance)",
    )
    parser.add_argument(
        "--phash-eps",
        type=int,
        default=8,
        help="DBSCAN eps for pHash features in bits (0-64); smaller is stricter",
    )

    args = parser.parse_args()
    in_dir = Path(args.input_dir).expanduser().resolve()
    if not in_dir.exists() or not in_dir.is_dir():
        print(f"[ERROR] Input directory not found: {in_dir}")
        sys.exit(1)

    if args.output_dir:
        out_dir = Path(args.output_dir).expanduser().resolve()
    elif args.task_name:
        out_dir = Path.cwd() / args.task_name
    else:
        out_dir = in_dir / "grouped_photos"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Scanning images under: {in_dir}")
    images = find_images(in_dir, exclude=out_dir)
    if not images:
        print("[ERROR] No images found.")
        sys.exit(1)
    print(f"[INFO] Found {len(images)} image(s)")

    pose_paths: List[Path] = []
    pose_features: List[np.ndarray] = []
    phash_paths: List[Path] = []
    phash_features: List[np.ndarray] = []

    use_pose = (args.method in ("pose", "auto")) and HAS_MEDIAPIPE
    if args.method == "pose" and not HAS_MEDIAPIPE:
        print("[WARN] MediaPipe not available; falling back to pHash.")

    for p in images:
        img = load_image(p)
        if img is None:
            print(f"[WARN] Skipping unreadable image: {p}")
            continue
        added = False
        if use_pose:
            fv = extract_pose_features(img)
            if fv is not None:
                pose_paths.append(p)
                pose_features.append(fv)
                added = True
        # Fallback or phash-only
        if not added or args.method == "phash":
            hv = phash_vector(img)
            phash_paths.append(p)
            phash_features.append(hv)

    next_folder_index = 1

    # Cluster pose-based features first (same pose grouping)
    if pose_features:
        print(f"[INFO] Clustering {len(pose_features)} images by pose with eps={args.pose_eps}")
        labels_pose = cluster_features(
            pose_features, metric="euclidean", eps=args.pose_eps, min_samples=args.min_cluster_size
        )
        next_folder_index = group_and_copy(pose_paths, labels_pose, out_dir, move=args.move, start_index=next_folder_index, input_dir=in_dir)
    else:
        if args.method == "pose":
            print("[WARN] No poses detected in any images; nothing clustered by pose.")

    # Cluster pHash-based features (visual similarity / near-duplicates)
    if phash_features:
        # Convert bits threshold to fraction for hamming distance
        phash_eps_frac = max(0.0, min(1.0, float(args.phash_eps) / 64.0))
        print(
            f"[INFO] Clustering {len(phash_features)} images by pHash with eps={args.phash_eps} bits ({phash_eps_frac:.3f} frac)"
        )
        labels_phash = cluster_features(
            phash_features, metric="hamming", eps=phash_eps_frac, min_samples=args.min_cluster_size
        )
        next_folder_index = group_and_copy(
            phash_paths, labels_phash, out_dir, move=args.move, start_index=next_folder_index, input_dir=in_dir
        )
    else:
        print("[INFO] No images available for pHash clustering.")

    print(f"[DONE] Grouped photos written to: {out_dir}")
    print("[NOTE] Clusters with label -1 are considered noise and not grouped.")
    print("[TIP] Tune --pose-eps and --phash-eps to adjust similarity strictness.")


if __name__ == "__main__":
    main()
