###example server code for local server
import socket
import threading
import time
import pickle


HEADER = 8 #pre-content of a message that specifies the num6er of 6ytes in the message
PORT = 5059
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PING_MESSAGE = "!PING"
chat_history = list()


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDRESS)


#handles client thread
#receives the message and message buffer, decodes and appends the message to the global message list
#sends the message list back to the client for display on the screen
def handle_client(conn,addr):

    print(f'new connection from {addr} connected')
    connected = True

    while connected:

        data_length = conn.recv(HEADER).decode(FORMAT) #unpacks the data_header from the client 
        data_length = int(data_length)
        msg = conn.recv(data_length).decode(FORMAT) #unpacks the data using the data_header from client

        if not msg: break 

    
        if msg == PING_MESSAGE:
            print("ping message received")
            chat_thread = threading.Thread(target = serve_ping_request, args = (conn,addr)) 
            chat_thread.start()
            continue


        if msg == DISCONNECT_MESSAGE: 
            connected = False

        chat_history.append((msg,addr))
        print(f'message received from {addr} is:  {msg}')
        print(f'current chat is {chat_history}')


    conn.close()


#returns the entire chat to the respective client
def serve_ping_request(conn,addr):
    pickled_chat = pickle.dumps(chat_history)
    pickled_chat_header = str((len(pickled_chat))).encode(FORMAT)
    pickled_chat_header += b' ' *(HEADER - len(pickled_chat_header)) #padding the header
    

    conn.send(pickled_chat_header)
    conn.send(pickled_chat)
    


#resets the chat history

#prints entire chat list
def print_chat():

    print(chat_history)


#updates the chat history
def update_chat(msg,addr):

    return chat_history.append((msg,addr))


#starts the server, accepts connections and starts a new thread for each client that connects
def start():

    chat_history = list()
    server_socket.listen()
    

    while True:
        conn,addr = server_socket.accept() 
        thread = threading.Thread(target = handle_client, args = (conn,addr)) 
        thread.start() 
        print(f'active connections {threading.activeCount() - 1} ') 


#starts the server
if __name__ == "__main__":
    print('server starting....')
    start()
