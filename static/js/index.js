// For the moment we are importing the socket.io.js file from the CDN
var socket = io();

startTest = () => {
    socket.emit('start_test');
}

socket.on('new_number', (arg) => {
    console.log(arg);
});