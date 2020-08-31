# This is a simple dummy client used to test the connection with the server.
#
# Created by xetiro (aka Ruben Geraldes) on 28/09/2020.
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connection successfully')

@sio.event
def disconnect():
    print('Disconnected successfully')

def sendImage(image):
    sio.emit('receiveImage', image)


sio.connect('http://0.0.0.0:9000') 

sendImage("testing sending images")