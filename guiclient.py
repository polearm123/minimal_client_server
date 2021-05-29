import socket,pickle,threading,time
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtgui

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

HEADER = 8
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5051

FORMAT = 'utf-8'

local_chat_history = list()

class ChatWorker(QObject):

    finished = pyqtSignal()
    chat = pyqtSignal(list)
    

    def __init__(self,client_socket,connected,message):

        super().__init__()
        self.client_socket = client_socket
        self.connected = connected
        self.message = message
        

    def run(self):
        
        if self.connected:

            string_buffer = self.message.encode(FORMAT)
            length = str(len(string_buffer))
            length_buffer = length.encode(FORMAT)
            length_buffer += b' '*(HEADER - len(length_buffer)) #pad one byte space to the buffer for every byte below the header size
            self.client_socket.send(length_buffer)
            self.client_socket.send(string_buffer)
            
        self.finished.emit()

    #retrieves the chat from server and emits it as a signal
    def retrieve_chat(self):

        updated_chat = self.ping()
        self.chat.emit(updated_chat)
        self.finished.emit()

    #pings server for server chat, compares it to current chat and returns it as a list
    #if there are no differences, noone has written anything and it will return an empty list
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
            return compared_chat

        else:
            return []

        
    #sets the local chat to the server chat
    def update_local_chat(self,updated_chat):

        global local_chat_history
        local_chat_history = updated_chat.copy()
        

    #compares local to server chat and returns the new additions as a list
    def compare_local_server_chat(self,server_chat):

        global local_chat_history
        new_messages_list = list()

        if local_chat_history == server_chat:
            return []

        else:
            for i in server_chat:
                if i not in local_chat_history:
                    new_messages_list.append(i)

        self.update_local_chat(server_chat)#updates the local chat to be equal to that of the server after retrieving new messages
        return new_messages_list



#class to define the graphical window inherits from QtWidget superclass
class MainWindow(qtw.QWidget):
    
    #initialises the window with labels and a text box
    def __init__(self):

        #initialise the client_socket for communication
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((HOST,PORT))
        self.connected = True

        super().__init__()

        #window title
        self.setWindowTitle("python chat client")


        #layout
        self.setLayout(qtw.QVBoxLayout())


        #adds appropriate buttons and text inputs
        text_input = qtw.QLineEdit()
        text_input.setObjectName("text_field")
        text_input.setText("")
        self.chat_frame = QListWidget()


        #initialises and starts a timer 
        #timer emits a signal every 1000 miliseconds that calls a function to 
        #retrieve the server chat, compare and update the local chat for view on gui
        self.timer = QTimer()
        self.timer.timeout.connect(self.retrieve_server_chat)
        self.timer.start(1000)
        

        #create a button to send message
        send_button = qtw.QPushButton("Send",clicked = lambda: send())

        #the chat frame is the viewable chat window
        chat_frame = qtw.QListWidget()

        #adds the widgets created above to the layout
        self.layout().addWidget(text_input)
        self.layout().addWidget(send_button)
        
        #shows the gui
        self.show()
        
        #sets the showing label to the text input and clears the text input
        def send():
            self.send_values(text_input.text())
            text_input.setText("")


    #alters the chat frame on the gui on each timeout signal
    #prints any changes between the server and client chat
    def alter_chat_frame(self,server_chat_list):

        for i in server_chat_list:
            self.chat_frame.addItem(f'{i[1]} says: {i[0]} \n')
        
        self.layout().addWidget(self.chat_frame)
        

    #starts a thread responsible for sending the chat messages to the server
    def send_values(self,chat):

        self.threadOne = QThread()
        self.workerOne = ChatWorker(self.client_socket,self.connected,chat)
        self.workerOne.moveToThread(self.threadOne)

        self.threadOne.started.connect(self.workerOne.run)
        self.workerOne.finished.connect(self.threadOne.quit)
        self.workerOne.finished.connect(self.workerOne.deleteLater)
        self.threadOne.finished.connect(self.threadOne.deleteLater)
        self.threadOne.start()


    #starts thread responsible for checking the differences between local chat 
    #and server chat, updating the local chat accordingly
    def retrieve_server_chat(self):

        self.threadTwo = QThread()
        self.workerTwo = ChatWorker(self.client_socket,self.connected,"none")
        self.workerTwo.moveToThread(self.threadTwo)
       

        self.threadTwo.started.connect(self.workerTwo.retrieve_chat)
        self.workerTwo.finished.connect(self.threadTwo.quit)
        self.workerTwo.finished.connect(self.workerTwo.deleteLater)
        self.threadTwo.finished.connect(self.threadTwo.deleteLater)
        self.workerTwo.chat.connect(self.alter_chat_frame)
        self.threadTwo.start()


if __name__ == "__main__":

    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec()
    