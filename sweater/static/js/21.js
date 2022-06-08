var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
type: 'bar',

date: {
labels: ["ex", "dss"],
datasets: [{
label: "fs",
backgroundColor: 'rgb(255, 99, 132)',
borderColor: 'rgb(255, 99, 132)',
data: [2, 2000],
}]
},
options: {}

});
