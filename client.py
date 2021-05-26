import socket,pickle,threading,time

HEADER = 8
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5059

FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

connected = True


#should ping, return and print the contents of the entire chat present at server
def ping():

    msg = '!PING'
    msg_header = str(len(msg)).encode(FORMAT)
    msg_header += b' ' * (HEADER-len(msg_header))
    string_buffer = msg.encode(FORMAT)
    client_socket.send(msg_header)
    client_socket.send(string_buffer)
    chat_content_header = int(client_socket.recv(HEADER).decode(FORMAT))
    chat_content = pickle.loads(client_socket.recv(chat_content_header))
    
    print(chat_content)


#threaded function that sends a ping to server to retrieve and print the list every second
def refresh_chat():

    while True:
        ping()
        time.sleep(1)



while connected:

    chat_thread = threading.Thread(target = refresh_chat)
    chat_thread.start()

    string = input("enter a message to send to the server\n")
    string_buffer = string.encode(FORMAT)
    length = str(len(string_buffer))
    length_buffer = length.encode(FORMAT)
    print(length_buffer)
    print(string_buffer)
    length_buffer += b' '*(HEADER - len(length_buffer)) #pad one byte space to the buffer for every byte below the header size
    print(f'length buffer after padding: {len(length_buffer)}')
    client_socket.send(length_buffer)
    client_socket.send(string_buffer)

    
    

