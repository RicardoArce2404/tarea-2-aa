from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import eventlet # eventlet is an asynchronous framework that works with Flask-SocketIO
from src.logic import get_solution

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start')
def start(limit):
    result = get_solution([randint(1, 100) for _ in range(10)], int(limit))
    print(result)

if __name__ == '__main__':
    socketio.run(app, debug=True)