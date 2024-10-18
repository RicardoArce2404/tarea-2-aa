// For the moment we are importing the socket.io.js file from the CDN
var socket = io();

// elements
const limitInput = document.getElementById('limit');
const setSpan = document.getElementById('set');
const generationSpan = document.getElementById('generation');
const bestSetSpan = document.getElementById('best-set');
const bestSum = document.getElementById('best-sum');
const startButton = document.getElementById('start-button');

startAlgorithm = () => {
    startButton.disabled = true;
    limit = limitInput.value;
    validInput = true
    if (limit == '') {
        alert('Por favor ingrese un número');
        validInput = false
    } else if (isNaN(limit)) {
        alert('Por favor ingrese un número válido');
        validInput = false
    } else if (parseInt(limit) < 1) {
        alert('Por favor ingrese un número mayor a 0');
        validInput = false
    }
    if (validInput) {
        socket.emit('start', limit);
    }
    startButton.disabled = false;
};

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('update-state', (args) => {
    startButton.disabled = true;
    setSpan.innerHTML = `{${args.set}}`;
    generationSpan.innerHTML = args.generation;
    bestSetSpan.innerHTML = `{${args.solution}}`;
    bestSum.innerHTML = '+' + args.sum;
});

socket.on('end', () => {
    startButton.disabled = false;
});