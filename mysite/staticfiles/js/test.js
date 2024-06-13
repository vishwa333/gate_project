
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

function Topic_Wise(this) {
  console.log('Getting Topics wise');
}
function Gate_Previous_Year(this){
  console.log('Getting PYQ wise');
}


document.addEventListener('DOMContentLoaded', function() {
  // Get all .test-type divs
  const testTypeDivs = document.querySelectorAll('.test-type');
  const count = testTypeDivs.length;
  // console.log("Items identified: "+count);
  // Loop through each div and add event listener
  testTypeDivs.forEach(function(div) {
    const overlay = div.querySelector('.test-overlay');

    // Add click event listener to the div
    div.addEventListener('click', function() {
      // Toggle the display property of the overlay
      if (overlay.style.display === 'none' || overlay.style.display === '') {
        overlay.style.display = 'flex';
        var fun_name = this.id.replaceAll(" ", '_');
        console.log("The ID is : ",fun_name)
        window[fun_name](this);
      } else {
        overlay.style.display = 'none';
      }
      
    });
  });

  
  //console.log('DOM fully loaded and parsed');
});