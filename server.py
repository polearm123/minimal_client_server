###example server code for local server
import socket
import threading
import time
import pickle


HEADER = 64 #pre-content of a message that specifies the num6er of 6ytes in the message
PORT = 5057
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDRESS)


#handles client thread
#receives the message and message buffer, decodes and appends the message to the global message list
#sends the message list back to the client for display on the screen
def handle_client(conn,addr):

    print(f'new connection from {addr} connected')
    connected = True

    while connected:

        data_length = conn.recv(64).decode(FORMAT) #unpacks the data from the client 
        data_length = int(data_length)
        msg = conn.recv(data_length).decode(FORMAT)

        if not msg: break 

        chat = update_chat(msg,addr)
        print(f'message received from {addr} is:  {msg}')

        pickled_chat = pickle.dumps(chat)
        pickled_chat_header = str((len(pickled_chat))).encode(FORMAT)
        print(pickled_chat_header)
        print(pickled_chat)

        conn.send(pickled_chat_header)
        conn.send(pickled_chat)

        if msg == DISCONNECT_MESSAGE: 
            connected = False

    conn.close()


#resets the chat history
def reset_chat():

    chat_history = list()


#prints entire chat list
def print_chat():

    print(chat_history)


#updates the chat history
def update_chat(msg,addr):

    chat_history.append((msg,addr))
    return chat_history


#starts the server, accepts connections and starts a new thread for each client that connects
def start():

    server_socket.listen()
    reset_chat()

    while True:
        conn,addr = server_socket.accept() 
        thread = threading.Thread(target = handle_client, args = (conn,addr)) 
        thread.start() 
        print(f'active connections {threading.activeCount() - 1} ') 


#starts the server
if __name__ == "__main__":
    print('server starting....')
    chat_history = list()
    start()
