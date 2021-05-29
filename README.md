# minimal_client_server

A brief project I took up to learn the basics of python sockets,python threads,QThreads and PyQt5 and just a refresher after taking a long break from programming

It contains the barebones functionality to facilitate communication between a server and client(s)
Also has a basic user interface using pyqt5 that allows the user to read all messages sent under the local network and send messages

Learning Objectives:

1. Refresher in python

2. Learn about sockets
  - client and server sockets
  - communication protocols between client(s) and server 
  - data packet headers and their importance
  - packaging and depackaging streams of information (pickle)
  
3. Basic, hands on pyqt5 experience
  - event driven development
  - Widgets, Windows and QT classes and how they interact with each other
  - custom signals and slots
  - QTimer for refreshing certain widgets on timeout
  
4. Basics of multithreading and it's importance
  - avoidance of race conditions and corrupting data
  - locking
  - how to use QThreads
  
 
 Installation instructions:
 
 1. clone the repository to local directory : $ git clone [url]
 2. create a python virtual environment: $ python -m venv [name of virtual environment]
 3. activate the virtual environment: $ source [name of virtual environment]/bin/activate
 4. make sure pip is up to date: $ pip install --upgrade pip
 5. install all required dependencies $ pip install -r requirements.txt
 6. run the server: python server.py
 7. Run client(s) using the gui: $ python guiclient.py
            - or the command line: $ python client.py
 8. Enjoy
 
 
 
 Features: (More coming)...
  
  -One single chat room that facilitates many connected clients 
