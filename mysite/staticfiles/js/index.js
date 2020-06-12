/* Load this function on page loads*/
/**/
/* Open when someone clicks on the span element */
function openNav() {
  /*document.getElementById("myNav").style.display = "block";*/
  document.getElementById("myNav").style.height = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
  /*document.getElementById("myNav").style.display = "none";
  window.alert("Cliked to close");*/
  abc();
  document.getElementById("myNav").style.height = "0";
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

window.onload = abc();