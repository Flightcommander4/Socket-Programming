# Matthew Calandrella - ECE 416 Assignment #1 (Server UDP)

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
CHUNK_MESSAGE = "ACK Received"

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
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', PORT))

#Start the server when the program is executed
def start():
    #Server will be listening...
    print(f"Server is Listening on {socket.gethostbyname(socket.gethostname())}...")

    print("[Active Connections: 1]")
    print("Waiting for file...")
    while True:
        
        #Find out what the User wants to do
        userCommand = server.recv(1024).decode(FORMAT)

        #When the user uploads a file, we handle it here
        if userCommand == 'put':
            
            #Receiving File Length
            fileLength, clientAddress = server.recvfrom(1000000)
            fileLength = fileLength.decode(FORMAT)
            print(f"File is of length {len(fileLength)}")
            currentFileChunk = b'0'
            
            while currentFileChunk != b"":
                #Receiving the Chunks
                currentFileChunk, clientAddress = server.recvfrom(1000)
                print("Chunk Received!")
                server.sendto(CHUNK_MESSAGE.encode(), clientAddress)
                currentFileChunk, clientAddress = server.recvfrom(1000)
            
            print("Waiting for Client Keyword...")

        #When the user sends through a keyword, we anonymize it in the target file
        if userCommand == 'keyword':
            #Receiving the keyword and decoding it
            keyword, clientAddress = server.recvfrom(2048)
            keyword = keyword.decode(FORMAT)
        
            print(f"Keyword Entered: {keyword}")
            server.sendto('Keyword Received'.encode(FORMAT), clientAddress)
            keywordFile = server.recv(100000).decode(FORMAT)

            #Taking the received data, and replacing the found keyword in the data with "X's" as to
            #anonymize the file with the associated keyword
            fileLength = re.sub(keyword, 'X'*len(keyword), fileLength, flags=re.IGNORECASE)
            print("Your File has been Anonymized!")
            
        
        #When the user enters get, the target file is downloaded by the client
        if userCommand == 'get':
            #Sends the anonymized file 
            server.sendto(fileLength.encode(FORMAT), clientAddress)
            print("Waiting for client...")
        
        #When the user enters quit, the client will disconnect and the server must know about this
        if userCommand == 'quit':
            disconnectMsg = server.recv(2048).decode(FORMAT)
            print(disconnectMsg)
            #Close the connection to the socket and exit the program
        
#Starting the server...
print("Starting Server...")
start()
