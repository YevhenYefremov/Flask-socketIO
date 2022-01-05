import time

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from datetime import datetime
from multiprocessing import Process, Queue

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')


def ladderVisibilityToggle():
    oldRes = ''
    while True:
        seconds = int(datetime.now().strftime('%S'))
        if seconds % 2 == 0:
            result = 'ladder2 hide'
        else:
            result = 'ladder2 show'
        if oldRes != result:
            try:
                socketio.emit(result, namespace='/', broadcast=True)
            except Exception as Ex:
                print('Can\'t send message: ' + result + '. Get exception: ' + Ex.__str__())
            finally:
                print("Request sended: " + result)
                oldRes = result


def appRun():
    socketio.run(app)


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    print('From app.route')
    return render_template('index.html')


if __name__ == '__main__':
    q = Queue()
    process_one = Process(target=appRun)
    process_two = Process(target=ladderVisibilityToggle)
    process_one.start()
    process_two.start()
    q.close()
    q.join_thread()
    process_one.join()
    process_two.join()
