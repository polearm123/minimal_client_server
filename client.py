import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((HOST,PORT))

connected = True

while connected:

    string = input("enter a message to send to the server\n")
    string_buffer = bytes(string, FORMAT)
    length = str(len(string_buffer))
    length_buffer = bytes(length, FORMAT)
   
    client_socket.sendall(length_buffer)
    client_socket.sendall(string_buffer)
    server_response = client_socket.recv(int(length)).decode(FORMAT)


    print(f'server responds: {server_response}')
    

