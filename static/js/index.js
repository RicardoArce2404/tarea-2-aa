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
    if (limit == '') {
        alert('Por favor ingrese un número');
        return;
    } else if (isNaN(limit)) {
        alert('Por favor ingrese un número válido');
        return;
    }
    socket.emit('start', limit);
};

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('update-state', (args) => {
    console.log(args);
    startButton.disabled = true;
    setSpan.innerHTML = `{${args.set.join(', ')}}`;
    generationSpan.innerHTML = args.generation;
    bestSetSpan.innerHTML = `{${args.solution.join(', ')}}`;
    bestSum.innerHTML = '+' + args.sum;
});

socket.on('end', () => {
    startButton.disabled = false;
});