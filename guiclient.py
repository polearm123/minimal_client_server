import socket,pickle,threading,time
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtgui

HEADER = 8
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5054

FORMAT = 'utf-8'

local_chat_history = list()


#class to define the graphical window inherits from QtWidget superclass
class MainWindow(qtw.QWidget):
    
    #initialises the window with labels and a text box
    def __init__(self):

        super().__init__()

        #window title
        self.setWindowTitle("python chat client")

        #layout
        self.setLayout(qtw.QVBoxLayout())

        #change font of the label

        #create a text input
        text_input = qtw.QLineEdit()
        text_input.setObjectName("text_field")
        text_input.setText("")


        #create a button to send message
        send_button = qtw.QPushButton("Send",clicked = lambda: send())

        #set the chat frame
        chat_frame = qtw.QVBoxLayout()

        self.layout().addWidget(text_input)
        self.layout().addWidget(send_button)
        self.layout().addWidget(chat_frame)

        #initialises client
        client = Client()
        client.client_start()

        #shows the created gui
        self.show()


        #sets time to respond to the updated chat caused by the client pings
        timer = QtCore.QTimer()
        timer.timeout.connect(update_gui_chat_label)
        timer.start(10000)

        
        #sets the showing label to the text input and clears the text input
        def send():
            my_label.setText(f'{text_input.text()}')
            text_input.setText("")


        #removes all widget labels and replaces them with the updated chat if there is an updated chat available
        def update_gui_chat_label():
            if not chat_frame.children():
                return

            else:
                for i in local_chat_history:
                    chat_widget = qtw.QLabel(f'{i}')
                    chat_frame.addWidget(chat_widget)







class Client:

    def __init__(self):

        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((HOST,PORT))
        self.connected = True


    #should ping, update and print the retrieves messages from the server
    def ping(self):
        
        msg = '!PING'
        msg_header = str(len(msg)).encode(FORMAT)
        msg_header += b' ' * (HEADER-len(msg_header))
        string_buffer = msg.encode(FORMAT)
        self.client_socket.send(msg_header)
        self.client_socket.send(string_buffer)
        chat_content_header = int(self.client_socket.recv(HEADER).decode(FORMAT))
        chat_content = pickle.loads(self.client_socket.recv(chat_content_header))
        
        compared_chat = self.compare_local_server_chat(chat_content) #compares local and server chat to return a list of new messages

        if compared_chat:
            # nice_tuples(compared_chat)
            return compared_chat

        
    #prints chat out in nice format
    def nice_tuples(self,list_of_tuples):

        for i in list_of_tuples:
            print(f'{i[1]} says: {i[0]}')


    #sets the local chat to the server chat
    def update_local_chat(self,updated_chat):

        global local_chat_history
        local_chat_history = updated_chat.copy()
        


    #compares local to server chat and returns the new additions as a list
    def compare_local_server_chat(self,server_chat):

        global local_chat_history
        new_messages_list = list()

        if local_chat_history == server_chat:
            return

        else:
            for i in server_chat:
                if i not in local_chat_history:
                    new_messages_list.append(i)

        self.update_local_chat(server_chat)#updates the local chat to be equal to that of the server after retrieving new messages

        return new_messages_list


    #threaded function that sends a ping to server to retrieve and print the list every second
    def refresh_chat(self):

        while True:
            self.ping()
            time.sleep(1)


    #sends messages from the client to the server
    #starts a thread that constantly pings the server for the updated chat
    def client_start(self):

        while self.connected:

            chat_thread = threading.Thread(target = self.refresh_chat) #thread 
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

    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec()
    