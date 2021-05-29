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
    chat = pyqtSignal(list())
    

    def __init__(self,client_socket,connected,message):
        super().__init__()
        self.client_socket = client_socket
        self.connected = connected
        

    def run(self):
        """Long-running task."""
        if self.connected:
            self.message = message
            string_buffer = self.message.encode(FORMAT)
            length = str(len(string_buffer))
            length_buffer = length.encode(FORMAT)
            # print(length_buffer)
            # print(string_buffer)
            length_buffer += b' '*(HEADER - len(length_buffer)) #pad one byte space to the buffer for every byte below the header size
            # print(f'length buffer after padding: {len(length_buffer)}')
            self.client_socket.send(length_buffer)
            self.client_socket.send(string_buffer)
            

        self.finished.emit()

    #retrieves the chat from server and emits it as a signal
    def retrieve_chat(self):
        print("inside retrieve chat")
        updated_chat = self.ping()
        self.chat.emit(updated_chat)
        self.finished.emit()

    #pings server for server chat, compares it to current chat and returns it as a list
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



#class to define the graphical window inherits from QtWidget superclass
class MainWindow(qtw.QWidget):
    
    #initialises the window with labels and a text box
    def __init__(self):

        
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((HOST,PORT))
        self.connected = True

    
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

        print("at timer")

        self.timer = QTimer()
        self.timer.timeout.connect(self.retrieve_server_chat)
        self.timer.start(50)

        print("after time")

        
        #create a button to send message
        send_button = qtw.QPushButton("Send",clicked = lambda: send())

        #set the chat frame
        chat_frame = qtw.QListWidget()


        
        self.layout().addWidget(text_input)
        self.layout().addWidget(send_button)
        self.layout().addWidget(chat_frame)

        # self.show()
        print("at show")
        




















        #sets time to respond to the updated chat caused by the client pings
        # timer = QtCore.QTimer()
        # timer.timeout.connect(update_gui_chat_label)
        # timer.start(10000)

        
        #sets the showing label to the text input and clears the text input
        def send():
            self.send_values(text_input.text())
            text_input.setText("")


        #response to the timer signal, calls another function that deals with retrieving the server chat(setting up a thread) and printing onto the chatframe


        #removes all widget labels and replaces them with the updated chat if there is an updated chat available
        def update_gui_chat_label():
            if not chat_frame.children():
                return

            else:
                counter = 0
                for i in local_chat_history:
                    chat_frame.insertItem(i,f'{local_chat_history[i]}')


    def alter_chat_frame(self,server_chat_list):
        self.chat_frame = QListWidget()
        print(server_chat_list)
        for i in server_chat_list:
            self.chat_frame.addItem(i)

            








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

    def retrieve_server_chat(self):
        print("at retrieve server chat")
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
    