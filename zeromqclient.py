### ZEROMQ CLIENT
import zmq
context = zmq.Context()
print('Connecting to server')
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print('Connected, message grabbing started')
while True:
    socket.send(b"OK")
    message = socket.recv()
    print(message)
