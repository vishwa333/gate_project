# AI Agent Instructions: gate_project

## Project map (two code areas)
- `mysite/`: legacy-style Django monolith (primary app code).
- `scripts/`: standalone utility scripts (currently photo grouping CLI).

## Django architecture (what matters first)
- Main project module: `mysite/mysite/` (`settings.py`, root `urls.py`).
- Three apps included at root path `''`: `my_test`, `accounts`, `questions`.
- URL inclusion order in `mysite/mysite/urls.py` matters; `my_test.urls` is first and owns index (`/`).
- Templates are centralized in `mysite/templates/` (not per-app template dirs).
- Static files come from `mysite/staticfiles/`; media is served in dev via `my_test/urls.py` + `static(...)`.

## Core domain model and flow
- `questions/models.py`: taxonomy + item bank (`subject` → `chapter` → `topic` → `question` + `solution`).
- `my_test/models.py`: test assembly (`test.questions`, `test.tsub`, `test.tchap`) and scoring persistence (`test_result`, `test_responses`).
- Runtime flow in `my_test/views.py`: browse tests (`tests`/`step2`/`step3`) → run (`start_test`/`get_question`) → save (`store_result`) → analytics (`view_result`).

## Auth and routing conventions (project-specific)
- Custom auth model is `accounts.models.my_user`; login uses email (`USERNAME_FIELD = 'email'`).
- `AUTH_USER_MODEL` in settings is `accounts.My_user` (case mismatch with class name); treat as a known project quirk before changing auth/migrations.
- Most protected views use explicit checks (`request.user.is_authenticated`) or helper `redirect_if_not_login()`.
- Routes are mostly unprefixed (`/signup`, `/tests`, `/store_result`, etc.); avoid introducing collisions across apps.

## Persistence and environment
- DB backend is `djongo` selected by `DJANGO_ENV` in `mysite/mysite/settings.py`.
  - `DJANGO_ENV=local` → local Mongo DB `mysite`.
  - non-local → Atlas-style `CLIENT` config placeholder.
- `dump/mysite/*.bson` and `dump/admin/*.bson` are restorable Mongo dumps.
- `mysite/db.sqlite3` exists but is not the active configured DB.

## Developer workflows found in repo
- Start Django app from `mysite/`: `python manage.py runserver`.
- Scaffolding hints in `django_commands` (`startproject`, `startapp`).
- Dependencies in `mysite/requirements.txt` include Django + image stack (`Pillow`, `ImageHash`, `numpy`, `scikit-learn`, optional `mediapipe`).

## Script subsystem (`scripts/group_photos.py`)
- CLI groups similar images into numbered folders using DBSCAN.
- Method pipeline: pose features via MediaPipe when available, with pHash fallback (`--method auto` default).
- Output precedence: `--output-dir` > `--task-name` (cwd folder) > `<input>/grouped_photos`.

## Implementation patterns to preserve
- Model classes are lowercase (`subject`, `test`, `my_user`); keep naming consistent when extending existing apps.
- `test_responses` enforces uniqueness on (`test_id`, `question_id`, `user_id`) — do not bypass this with duplicate inserts.
- When adding authenticated pages in `my_test`, mirror existing guard + template pattern:
  - URL in `my_test/urls.py`
  - View in `my_test/views.py`
  - Template in `mysite/templates/`

If any section is unclear or missing (especially auth-model casing, Mongo setup, or URL-collision risks), share feedback and I will refine this file.