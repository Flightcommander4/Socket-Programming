# Matthew Calandrella - ECE 416 Assignment #1 (Server TCP)

#Importing Libraries
from os import read
import socket
import sys
import re

#Defining Variables and Other Useful Information
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[1])
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnected"

#*************************************************************************************
#  Title: Python Socket Programming Tutorial!
#  Author: Tech With Tim
#  Date: April 5th, 2020
#  Version: Python 3.0
#  Availability: https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
#*************************************************************************************

#************************************************************************************************************************************
#  Stack Overflow Links Used for Guidance:
#  Reading in Binary: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
#  Error Help: https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
#  UDP Help: https://stackoverflow.com/questions/27893804/udp-client-server-socket-in-python
#  TCP Help: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
#************************************************************************************************************************************

#Creating a new Socket, and Defining the Method of Streaming the Data.  As well as binding the 
#server to the given address and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', PORT))

#Start the server when the program is executed
def start():
    server.listen() #Server will be listening on the specified IP
    print(f"Server is Listening on {socket.gethostbyname(socket.gethostname())}...")
    
    #Accepts the connection from the client
    conn, addr = server.accept()
    print("[Active Connections: 1]")
    print("Waiting for file...")

    #While a connection is established, this will occur
    while True:
        
        #Find out what the User wants to do
        userCommand = conn.recv(1024).decode(FORMAT)

        #When the user uploads a file, we handle it here
        if userCommand == 'put':
            #Receive the incoming file, and decode it back into type "str"
            currentFile = conn.recv(100000).decode(FORMAT)
            print("File Received!")
            print("Waiting for keyword...")

        #When the user sends through a keyword, we anonymize it in the target file
        if userCommand == 'keyword':
            #Receiving the keyword and decoding it
            keyword = conn.recv(2048).decode(FORMAT)
        
            print(f"Keyword Entered: {keyword}")
            conn.send('Keyword Received'.encode(FORMAT))
            keywordFile = conn.recv(100000).decode(FORMAT)

            #Taking the received data, and replacing the found keyword in the data with "X's" as to
            #anonymize the file with the associated keyword
            keywordFile = re.sub(keyword, 'X'*len(keyword), keywordFile, flags=re.IGNORECASE)
            print("Your File has been Anonymized!")
            

        #When the user enters get, the target file is downloaded by the client
        if userCommand == 'get':
            #Sends the anonymized file
            conn.send(keywordFile.encode(FORMAT))
            print("Waiting for client...")

        #When the user enters quit, the client will disconnect and the server must know about this
        if userCommand == 'quit':
            disconnectMsg = conn.recv(2048).decode(FORMAT)
            print(disconnectMsg)
            print('User has Disconnected')
            #Close the connection to the socket and exit the program
    
#Starting the server...
print("Starting Server...")
start()
