function changeContent(menuItem, menuItemText) {
  // Show loading overlay
  var loadingOverlay = document.getElementById('loadingOverlay');
  loadingOverlay.style.display = 'flex';

  // Remove 'active' class from all menu items
  var menuItems = document.querySelectorAll('.test-menu-item');
  menuItems.forEach(function(item) {
    item.classList.remove('active');
  });

  // Add 'active' class to the clicked menu item
  menuItem.classList.add('active');

  // Update the content based on the clicked menu item
  var content = document.getElementById('test-content');
  var fun_name = menuItemText.replaceAll(" ", '_');
  console.log("The ID is : ",fun_name)
  var to_display = window[fun_name](content); 
  console.log(to_display)
  setTimeout(function() {
    content.innerHTML = to_display;
    populateChapters($("#chapter"), mathChapters);
    // $.getScript('staticfiles/js/topic_wise.js');
    // Hide loading overlay after transition is complete
    loadingOverlay.style.display = 'none';
  }, 1000); // Simulating a 1 second delay for demonstration
}

function get_subjects() {
  console.log('Getting Subjects');
  $.ajax({
    async: false,
    type: 'GET',
    url: '/get_subjects_list',
    success: function(data) {
         //callback
         return data;
    }
});
}

function get_chapters() {
  console.log('Getting Chapters');
  $.ajax({
    async: false,
    type: 'GET',
    url: '/get_chapters_list',
    data :{"subject":subject},
    success: function(data) {
         //callback
         return data;
    }
});
}

function Topic_Wise(element) {
  console.log('Change in any Topic_wise should be detected here');
  // Building the page with a given layout
  console.log(element.innerHTML)
  var result = ""
  $.ajax({
    async: false,
    type: 'GET',
    url: '/get_initial_topic_wise',
    success: function(data,element) {
         //callback
         console.log(data);
         result = data;
    }
    
    });
    return result;
}

function Gate_Previous_Year(){
  console.log('Getting PYQ wise');
}