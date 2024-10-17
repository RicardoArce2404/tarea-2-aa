// For the moment we are importing the socket.io.js file from the CDN
var socket = io();

// elements
const limitInput = document.getElementById('limit');

startAlgorithm = () => {
    limit = limitInput.value;
    if (limit == '') {
        alert('Por favor ingrese un número');
        return;
    } else if (isNaN(limit)) {
        alert('Por favor ingrese un número válido');
        return;
    }
    socket.emit('start', limit);
}

socket.on('update-state', (arg) => {
    console.log(arg);
});