import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((HOST,PORT))

connected = True

while connected:

    string = input("enter a message to send to the server\n")
    string_buffer = string.encode(FORMAT)
    length = str(len(string_buffer))
    length_buffer = length.encode(FORMAT)
   
    client_socket.send(length_buffer)
    client_socket.send(string_buffer)

    server_response = client_socket.recv(int(length)).decode(FORMAT)

    print(f'server responds: {server_response}')
    

