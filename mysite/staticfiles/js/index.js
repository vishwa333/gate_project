/* Load this function on page loads*/
/**/
/* Open when someone clicks on the span element */
function openNav() {
  /*document.getElementById("myNav").style.display = "block";*/
  document.getElementById("overlay").style.height = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
  /*document.getElementById("myNav").style.display = "none";
  window.alert("Cliked to close");*/
  abc();
  document.getElementById("overlay").style.height = "0";
}
function abc() {
  /*window.alert("Clicked/Loaded");*/
};
function showlogin(){
    $(".signup").css("visibility", "hidden");
    $(".login").css("visibility", "visible");
    $(".loginbut").css({"background-color":"#ffffff"});
    $(".signupbut").css({"background-color":"#dbdbdb"});
}

function showsignup(){
    $(".login").css("visibility", "hidden");
    $(".signup").css("visibility", "visible");
    $(".signupbut").css({"background-color":"#ffffff"});
    $(".loginbut").css({"background-color":"#dbdbdb"});
}

document.addEventListener('DOMContentLoaded', function() {
  const loginBtn = document.getElementById('login-btn');
  const overlay = document.getElementById('overlay');
  const closeBtn = document.querySelector('.close-btn');
  const signupLink = document.getElementById('signup-link');
  const loginLink = document.getElementById('login-link');
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  loginBtn.addEventListener('click', function() {
      overlay.style.display = 'flex';
  });

  closeBtn.addEventListener('click', function() {
      overlay.style.display = 'none';
  });

  signupLink.addEventListener('click', function() {
      loginForm.style.display = 'none';
      signupForm.style.display = 'block';
  });

  loginLink.addEventListener('click', function() {
      signupForm.style.display = 'none';
      loginForm.style.display = 'block';
  });

  window.addEventListener('click', function(event) {
      if (event.target === overlay) {
          overlay.style.display = 'none';
      }
  });
});


window.onload = abc();