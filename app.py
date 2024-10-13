from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import eventlet # eventlet is an asynchronous framework that works with Flask-SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

# this is a test that prints a random number every second
# to the console and emits it to the client
# the client will display the number in the console as well
@socketio.on('start_test')
def start_test():
    print('Test started')
    for i in range(10):
        eventlet.sleep(1) # IMPORTANT! we use eventlet.sleep instead of time.sleep!!
        random_number = randint(1, 100)
        print('Random number:', random_number)
        socketio.emit('new_number', random_number)

if __name__ == '__main__':
    socketio.run(app, debug=True)