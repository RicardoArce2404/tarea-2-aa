from flask import Flask, render_template
from src.socketio_setup import app, socketio
from random import randint
import eventlet # eventlet is an asynchronous framework that works with Flask-SocketIO
from src.logic import get_solution

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start')
def start(limit):
    socketio.emit('hello-world')
    try:
        limit = int(limit)
        result = get_solution([randint(1, limit) for _ in range(32)], limit)
    except ValueError:
        print(f"[Log] Attempted to use a non-integer value: {limit}.")
    socketio.emit('end')

if __name__ == '__main__':
    socketio.run(app, debug=True)