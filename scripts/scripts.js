// script.js
document.addEventListener('DOMContentLoaded', function() {
    
});


//Function for the slider

const slider = document.getElementById('rangeSlider');
const sliderValue = document.getElementById('sliderValue');

const stepLabels = ["3 dag", "1 dag", "60 min", "30 min", "10 min"];

const step24hours = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00,','08:00','09:00','10:00','11:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00']

slider.addEventListener('input', function() {
  const step = slider.value;
  sliderValue.textContent = stepLabels[step];
});

