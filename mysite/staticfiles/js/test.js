
o1 = -1;
function abc() {
  //window.alert("Clicked/Loaded");
  document.getElementById("home").className = "w3-bar-item w3-button w3-right";
  document.getElementById("tests").className = "active w3-bar-item w3-button w3-right";
};
// Get the modal
var stest = document.getElementById("show_test");
// Get the button that opens the modal
var btn = document.getElementById("myBtn");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// When the user clicks the button, open the modal
$(document).on('click','#myBtn',function(){
    // Get the modal
    var stest = document.getElementById("show_test");
    //window.alert("Yes");
    stest.style.display = "block";
});

// When the user clicks on <span> (x), close the modal

$(document).on('click','.last',function(){
  var stest = document.getElementById("show_test");
  stest.style.display = "none";
});
var ttype=-1
$(document).on('click','.ttype',function(){
    o1 = this.value
    /*$("#filtertable").empty();
    window.alert(this.value);
    var div = $("<div id='tbutton'>HELLO WORLD</div>").hide();
    $(".tbutton") .fadeOut();
    window.location.replace("/select_test");
    $.get("/step2",{"o1":this.value},function(data){
        window.alert(data);
     });*/
     $.ajax({
     async: false,
     type: 'GET',
     url: '/step2',
     data:{"o1":this.value},
     success: function(data) {
          //callback

          var res = $(data).filter('#filters').html();
          window.alert(res);
          $("#filtertable").html(res);
     }
});
     on_custom_select();
});

$(document).on('click',"#get_test",function(){
    var sub = $("#sub").children("option:selected").val();
    var diff = $("#diff").children("option:selected").val();
    window.alert("Clicked to get test "+o1+" "+sub+" "+diff);
    $.ajax({
     async: false,
     type: 'GET',
     url: '/step3',
     data:{"o1":o1,"sub":sub,"diff":diff},
     success: function(data) {
          //callback
          window.alert(data);
          $(".third").html(data);
        }
     });
});

$(document).on('click',".take_test",function(){
    var id = $(this).attr('id');
    window.alert("clicked to take test "+id);
    /*$().redirect("/start_test.html",{"test_id":id});*/
});

$(document).on('click',".view_result",function(){
    var id = $(this).attr('id');
    window.alert("clicked to view result "+id);
    /*$().redirect("/start_test.html",{"test_id":id});*/
});

window.onload = abc();



function closeAllSelect(elmnt) {
  /*a function that will close all select boxes in the document,
  except the current select box:*/
  var x, y, i, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  for (i = 0; i < y.length; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < x.length; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);

function on_custom_select(){
window.alert("Called Custom select");
var x, i, j, selElmnt, a, b, c;
/*look for any elements with the class "custom-select":*/
x = document.getElementsByClassName("custom-select");
for (i = 0; i < x.length; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  /*for each element, create a new DIV that will act as the selected item:*/
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /*for each element, create a new DIV that will contain the option list:*/
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < selElmnt.length; j++) {
    /*for each option in the original select element,
    create a new DIV that will act as an option item:*/
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /*when an item is clicked, update the original select box,
        and the selected item:*/
        var y, i, k, s, h;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        h = this.parentNode.previousSibling;
        for (i = 0; i < s.length; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            for (k = 0; k < y.length; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      /*when the select box is clicked, close any other select boxes,
      and open/close the current select box:*/
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
}