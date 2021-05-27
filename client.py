import socket,pickle,threading,time

HEADER = 8
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5054

FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

connected = True

local_chat_history = list()


#should ping, update and print the retrieves messages from the server
def ping():
    
    msg = '!PING'
    msg_header = str(len(msg)).encode(FORMAT)
    msg_header += b' ' * (HEADER-len(msg_header))
    string_buffer = msg.encode(FORMAT)
    client_socket.send(msg_header)
    client_socket.send(string_buffer)
    chat_content_header = int(client_socket.recv(HEADER).decode(FORMAT))
    chat_content = pickle.loads(client_socket.recv(chat_content_header))
    
    compared_chat = compare_local_server_chat(chat_content) #compares local and server chat to return a list of new messages

    if compared_chat:
        nice_tuples(compared_chat)
    
#prints chat out in nice format
def nice_tuples(list_of_tuples):

    for i in list_of_tuples:
        print(f'{i[1]} says: {i[0]}')


#sets the local chat to the server chat
def update_local_chat(updated_chat):

    global local_chat_history
    local_chat_history = updated_chat.copy()
    


#compares local to server chat and returns the new additions as a list
def compare_local_server_chat(server_chat):

    global local_chat_history
    new_messages_list = list()

    if local_chat_history == server_chat:
        return

    else:
        for i in server_chat:
            if i not in local_chat_history:
                new_messages_list.append(i)

    update_local_chat(server_chat)#updates the local chat to be equal to that of the server after retrieving new messages

    return new_messages_list


#threaded function that sends a ping to server to retrieve and print the list every second
def refresh_chat():

    while True:
        ping()
        time.sleep(1)


#sends messages from the client to the server
#starts a thread that constantly pings the server for the updated chat
def client_start():

    while connected:

        chat_thread = threading.Thread(target = refresh_chat) #thread 
        chat_thread.start()

        string = input()
        string_buffer = string.encode(FORMAT)
        length = str(len(string_buffer))
        length_buffer = length.encode(FORMAT)
        # print(length_buffer)
        # print(string_buffer)
        length_buffer += b' '*(HEADER - len(length_buffer)) #pad one byte space to the buffer for every byte below the header size
        # print(f'length buffer after padding: {len(length_buffer)}')
        client_socket.send(length_buffer)
        client_socket.send(string_buffer)

    
    
if __name__ == "__main__":

    client_start()