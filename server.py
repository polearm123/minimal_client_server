###example server code for local server
import socket
import threading
import time

HEADER = 64 #pre-content of a message that specifies the num6er of 6ytes in the message
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDRESS)

#handles client, paramters are retrieved after the server_socket receieves a client
def handle_client(conn,addr):
    print(f'new connection from {addr} connected')
    connected = True
    while connected:
        data_length = conn.recv(64).decode(FORMAT) #unpacks the data from the client 
        data_length = int(data_length)
        msg = conn.recv(data_length).decode(FORMAT)
        if not msg: break #breaks if there is no information from the client
        print(f'message received from {addr} is:  {msg}')
        conn.sendall(bytes(msg,FORMAT))#sends all the data back to the client

        if msg == DISCONNECT_MESSAGE: #checks when the client has disconnected
            connected = False

    conn.close()


#starts the server, accepts connections and starts a new thread for each client that connects
def start():

    server_socket.listen()
    while True:
        conn,addr = server_socket.accept() #stores information of client and connection ovject, allowing to send data
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f'active connections {threading.activeCount() - 1} ') #how many threads are active, 1 thread is always active, the start



print('server starting')
start()
