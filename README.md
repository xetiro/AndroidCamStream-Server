# AndroidCamStream-Server
A prototype server aplication that receives images frames, at a given frequency (i.e. 1hz, 2hz, 5hz, etc) from clients (AndroidCamStream-Client). The main client/server communication is done through websockets. Both the client and server makes use of the socket.io API.

## Quick Overview

### Motivation
This application was developed as a prototype server application (AndroidCamStream-Server), to allow to experiment with the use-case of client/server image stream processing, where the user's mobile device (AndroidCamStream-Client) is the source of the frames and this server is where the images are received for further processing.

### User Interaction
It is possible to launch the server from the command-line with several different options that defines the behavior of the server.

## In-memory user database

// TODO

## How to run
Running the server is pretty simple and can be done from the command-line. But since this is a client/server use-case you will also need to have an instance of the client application AndroidCamStream-Client running, so you can properly test the receiving of real image frames. Please visit the repo of the AndroidCamStream-Client for more information on the client-side.

### Requirements and Dependecies
The server application runs in the python3 environment and have the following dependencies:

- socket.io 4.6
  - `pip install python-socketio`
- eventlet 0.26
  - `pip install eventlet`
- opencv 4.4
  - `pip install opencv-python`

### Running the server
- Clone the project source-code to your local machine.
- Open the command-line and cd to the src folder of the project.
  - The source folder contains the ImageServer.py file which is where the server is implemented.
- Type `python3 ImageServer.py` to run the server in its simplest form. You should see the server initializing like this:
  - `(18351) wsgi starting up on http://0.0.0.0:8080`
  - This means the server was launched with the default hardcoded ips and ports. 
  - This also means that the server is not authenticating user credentials, so any username/password will be accepted (this is just intended for quick testing).
  - This also means that the server is not displaying any of the received images (this is ideal if you don't have any GUI OS, and just wanna do image processing).

### Different command options for launching the server
The short command explained is very limited. You can launch the server in a more meaningful by making use of the following options:

- `-i <server_ip>` or `--ip <server_ip>`
  - Sets the ip address the server is "running" on to server_ip that follows the option.
  - This is typically either the localhost (i.e. 127.0.0.1) or the real machine ip (e.g. 192.154.1.12)
  - Example: `python3 ImageServer.py -i 192.154.1.12` will translate to the following server address `http://192.154.1.12:8080`.
- `-p <server_port>` or `--port <server_port>`
  - Sets the port the server is listening to.
  - This is typically any port from 5000 up.
  - Example: `python3 ImageServer.py -p 9595` will translate to the following server address `http://0.0.0.0:9595`
- `-a` or `-auth`
  - Tells the server to authenticate the user's useraname/password credentials.
  - Example: `python3 ImageServer.py -a` will start the server at default ip and port but performing user's authentication upon new connections.
- `-d` or `--display`
  - Tells the server to display the frames received by each user on its own GUI window.
  - Example: `python3 ImageServer.py -d` will start the server at default ip and port but rendering the received frames of each user into a dedicated window.

Notice that all commands have a short version like in `-i` or long version like in `--ip`. They have exactly the same meaning for the server. 

### Recommended commands to launch the server
Although, you have some options at your disposal to launch the server with different configurations, at the end of the day I recommend you the following ways:

- `python3 ImageServer.py -i <server_ip> -p <server_port>` This is the most useful to testing with real clients. 
  - Example: `python3 ImageServer.py -i 192.154.1.12 -p 9595` will launch your server on the following address `http://192.154.1.12:9595`. Assuming that 192.154.1.12 is the real machine IP, a real client will use this address to connect with your server.
   - This example doesn't require authentication, so any client username/password will be accepted.
   - This example doesn't render any of the received frames. This is recommended if you just wanna do some background image processing, as rendering the user's frames on a GUI Window reduces your server performance. You should only launch the server with `-d` option if you wanna test that you are receiving the frames as you expect.
 - `python3 ImageServer.py -i <server_ip> -p <server_port> -a` This is the same as above but includes authentication of the users login.
   - Example: `python3 ImageServer.py -i 192.154.1.12 -p 9595 -a` will launch your server on the following address `http://192.154.1.12:9595` and it will check for the user's credentials when requesting to login with the server. Assuming that 192.154.1.12 is the real machine IP, a real client will use this address to connect with your server. Clients that don't have valid credentials with the server will be rejected.

## License
The sourcecode of this project is public under the MIT license. Feel free to fork it and change it at your will to customized it to your own projects.

> The MIT License is short and to the point. It lets people do almost anything they want with your project, like making and distributing closed source versions.
