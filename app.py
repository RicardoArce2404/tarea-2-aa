from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_test')
def start_test():
    print('Test started')
    for i in range(10):
        time.sleep(1)
        random_number = randint(1, 100)
        print('Random number:', random_number)
        socketio.emit('new_number', random_number)

if __name__ == '__main__':
    socketio.run(app, debug=True)