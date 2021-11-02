# Matthew Calandrella - ECE 416 Assignment #1 (Server UDP)

#Importing Libraries
from os import read
import socket
import threading
import sys

#Defining Variables and Other Useful Information
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12100 #int(sys.argv[1])
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

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', PORT))

def start():
    print(f"Server is Listening {''}")
    while True:
        
         #Find out what the User wants to do
        userCommand = server.recv(1024).decode(FORMAT)

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

        if userCommand == 'keyword':
            #Receiving the keyword and decoding it
            keyword, clientAddress = server.recvfrom(2048)
            keyword = keyword.decode(FORMAT)
        
            print(f"Keyword Entered: {keyword}")
            server.sendto('Keyword Received'.encode(FORMAT), clientAddress)
            keywordFile = server.recv(100000).decode(FORMAT)

            #Taking the received data, and replacing the found keyword in the data with "X's" as to
            #anonymize the file with the associated keyword
            fileLength = fileLength.replace(keyword, 'X'*len(keyword))
            print("Your File has been Anonymized!")
            server.sendto(fileLength.encode(FORMAT), clientAddress)
        
        if userCommand == 'get':
            #Waits for the Disconnect Message
            print("Waiting for client...")
        
        if userCommand == 'quit':
            disconnectMsg = server.recv(2048).decode(FORMAT)
            print(disconnectMsg)
            #Close the connection to the socket and exit the program
        

print("Starting Server...")
start()
