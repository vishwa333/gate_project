function openOverlay() {
  document.getElementById('overlay').style.display = 'block';
}

function closeOverlay() {
  document.getElementById('overlay').style.display = 'none';
}

function showSignup() {
  document.getElementById('login-form').classList.add('hidden');
  document.getElementById('signup-form').classList.remove('hidden');
}

function showLogin() {
  document.getElementById('signup-form').classList.add('hidden');
  document.getElementById('login-form').classList.remove('hidden');
}
