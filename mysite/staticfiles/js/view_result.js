$(document).on('click',".table_button",function(){
    alert("clicked"+this.value);
});

function first(){
    //var ctx = document.getElementById('myChart').getContext('2d');
    var ctx = $("#myChart");
    var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: [
            'Not-Attempted',
            'Attempted',
            'Correct',
            'Wrong',
          ],
        datasets: [{
          data: [10, 20, 0, 0],
          backgroundColor: [
            'blue',
            'lightgrey',
            'green',
            'red',
          ],
          labels: [
            'Not-Attempted',
            'Attempted',
            'Correct',
            'Wrong',
          ]
        }, {
          data: [10, 0, 15, 5],
          backgroundColor: [
            "rgba(255, 10, 13, 0)",
            'lightgrey',
            'green',
            'red',
          ],
          labels: [
            'Not-Attempted',
            'Attempted',
            'Correct',
            'Wrong',
          ]
        }, ]
      },
      options: {
        responsive: true,
        legend: {
          display: true,
          position:'bottom',
          align:'end',
        },
        tooltips: {
        	callbacks: {
          	label: function(tooltipItem, data) {
              var dataset = data.datasets[tooltipItem.datasetIndex];

              var sum=0;
              for(i=0;i<dataset.data.length;i++){
                sum += dataset.data[i];
              }
              //alert(sum)
              var index = tooltipItem.index;
              var percent = (dataset.data[index]*100)/sum;
              //alert(percent)

              return dataset.labels[index] + ': ' + dataset.data[index]+" : "+percent.toFixed(2)+"%";
            }

          }
        }
      }
    });

};



$(document).ready(function() {
  alert('Page is loaded');
  first();
});