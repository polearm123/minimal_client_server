import socket,pickle

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5057

FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((HOST,PORT))

connected = True

while connected:

    string = input("enter a message to send to the server\n")
    string_buffer = string.encode(FORMAT)
    length = str(len(string_buffer))
    length_buffer = length.encode(FORMAT)
    print(length_buffer)
    print(string_buffer)
    client_socket.send(length_buffer)
    client_socket.send(string_buffer)

    server_response_header = int(client_socket.recv(HEADER).decode(FORMAT))
    print(server_response_header)

    server_response = pickle.loads(client_socket.recv(server_response_header))

    print(f'server response header: {server_response_header}')
    print(f'server response message:{server_response}')
    

