# This is a simple prototype server to receive stream of pictures from the 
# AndroidCamStream client app.
# 
# This server is implemented with the socket.io framework that provides a
# easy-to-use of WebSockets. Therefore, this is a SYNCHRONOUS client/server.
# 
# PLEASE NOTICE: 
# The choice of synch client/server was intended for quick prototyping. However, 
# due to the nature of the video-streaming use-case a more robust implementation
# based on ASYNCHRONOUS client/server communication is strongly recommended. 
# Socket.io also provides an asynch server API.
#
# Created by xetiro (aka Ruben Geraldes) on 28/09/2020.
import sys, getopt
import eventlet
import socketio
import cv2
import numpy as np
from engineio.payload import Payload

# Default is 16 which can create a bootleneck for video streaming
Payload.max_decode_packets = 256

sio = socketio.Server()
app = socketio.WSGIApp(sio)

# Default server IP and server Port
ip = "0.0.0.0" 
port = 8080

# Display the image on a OpenCV window
isDisplay = False

# Use authentication to validate users
isAuth = False

# Dummy in-memory key-value pairs user database for dummy authentication using 
# plain-text passwords. Users credentials are username:password key-values
# WARNING: Never use plain-text passwords on a real application.
dummyUserDB = { 

    # Add more users as needed
    "user1": "pass1",
    "user2": "pass2",
    "Alice": "123",
    "Bob": "456"
    
}

# Map authenticated sessions id with usernames for display reasons
activeSessions = {}

@sio.event
def connect(sid, environ):
    print('connect', sid)
    print(activeSessions)

# Method used for user "dummy" authentication using an in-memory dummy database. 
# This can be used to authenticate the user with other server/service.
# WARNING: never use plain-text passwords on a real application.
@sio.event
def authenticate(sid, username, password, clientCallbackEvent):
    user = dummyUserDB.get(username)
    if isAuth == False or (user is not None and user == password):
        # add username to the session
        activeSessions[sid] = username
        sio.emit(clientCallbackEvent, True)
        print("User [" + username +"] authenticated.")
    else:
        sio.emit(clientCallbackEvent, False)
        sio.sleep(1)
        sio.disconnect(sid)
        print("User [" + username +"] authentication failed.")

# This is the main method that the client calls when streaming the pictures to 
# the server. Each receiveImage event is already processed in a new thread.
# The image format is JPEG and is sent by the client in as binary data of byte[] 
# received in python as Bytes.
@sio.event
def receiveImage(sid, imageBytes):
    # Process the image here or send image to another server here
    print(len(imageBytes))
    if(isDisplay):
        display(activeSessions[sid], bytes(imageBytes))

@sio.event
def disconnect(sid):
    print('disconnect', sid)
    activeSessions.pop(sid, None)
    print(activeSessions)
    if(isDisplay):
        # Avoids to keep a freezing window in case you used the show method
        cv2.destroyAllWindows()

def showImage(username, imageBytes):
    # Decode image from bytes
    nparr = np.frombuffer(imageBytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Show image after decoded
    cv2.imshow("Image Stream from " + username, img)
    cv2.waitKey(1)

def executeCommandArgs(argv):
    global ip, port, isDisplay, isAuth
    scriptName = argv[0]
    try:
        opts, args = getopt.getopt(argv[1:], "adhi:p:", ["ip=", "port=", "display", "auth"])
    except getopt.GetoptError: # wrong commands
        print(scriptName + " -i <server_ip> -p <server_port>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h": # help command
            print(scriptName + " -i <server_ip> -p <server_port")
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-d", "--display"):
            isDisplay = True
        elif opt in ("-a", "--auth"):
            isAuth = True

if __name__ == '__main__':
    executeCommandArgs(sys.argv)
    eventlet.wsgi.server(eventlet.listen((ip, port)), app)