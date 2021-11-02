# Matthew Calandrella - ECE 416 Assignment #1 (Client UDP)

#Importing Libraries
import socket
import sys

#Defining Variables and Other Useful Information
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname()) #int(sys.argv[1])
PORT = 12100  #int(sys.argv[2])
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "User has Disconnected"
CHUNK_MESSAGE = "ACK Received"


#*************************************************************************************
#  Title: Python Socket Programming Tutorial!
#  Author: Tech With Tim
#  Date: April 5th, 2020
#  Version: Python 3.0
#  Availability: https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
#*************************************************************************************

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((SERVER, PORT))
client.settimeout(1.0)


#print("Ready to Send Data")
#client.sendto(bytes(input(), FORMAT), (SERVER, PORT))
#newMsg, serverAddress = client.recvfrom(1024)
#print(newMsg.decode(FORMAT) + ' from ' + str(serverAddress))

while True:

    command = input(str("Enter Command: "))
    commandLine = command.split(" ")
    userCommand = commandLine[0]
    print('Awaiting Server Response')

    if commandLine[0] == 'put':
        client.send(userCommand.encode(FORMAT))
        #Getting File Size and Printing it
        fileName = commandLine [1]
        fileOpen = open(fileName, 'rb')
        fileReadLength = fileOpen.read()
        print(f'Length in Bytes is: {len(fileReadLength)}')
        client.sendto(fileReadLength, (ADDR))
        fileOpen.close
        print('Sending File...')
        fileRead = b'0'

        with open(fileName, 'rb') as fileOpen:
            #Sending the Chunks
            empty = ''
            fileRead = fileOpen.read(1000)
            print(f'Length of Chunk is: {len(fileRead)}')
            
            while fileRead != b"":
                client.sendto(fileRead, (ADDR))
                ackMsg, serverAddress = client.recvfrom(1024)
                print(ackMsg.decode(FORMAT))
                fileRead = fileOpen.read(1000)
                print(f'Length of Chunk is: {len(fileRead)}')
                client.sendto(fileRead, (ADDR))
                
        
        print('Done Sending File')


    if commandLine[0] == 'keyword':
        client.sendto(userCommand.encode(FORMAT), ADDR)
        keyword = commandLine[1]
        keywordFile = commandLine[2]
        client.send(keyword.encode(FORMAT))
        keywordMsg, serverAddress = client.recvfrom(10000)
        keywordMsg = keywordMsg.decode(FORMAT)
        
        if keywordMsg == 'Keyword Received':
            file = open(keywordFile, 'rb')
            fileread = file.read()
            while(fileread):
                client.send(fileread)
                fileread = file.read()
            file.close()
            newFile = keywordFile.split(".")
            print(f'Server Response: {keywordFile} has been anonymized, Output is {newFile[0]}_anon.txt')
    
    if commandLine[0] == 'get':
        client.send(userCommand.encode(FORMAT))
        newFile = keywordFile.split(".")
        anonText = client.recv(100000).decode(FORMAT)
        anonFile = open(newFile[0] + "_anon.txt", 'w')
        anonFile.write(anonText)
        print(f"File {newFile[0]}_anon.txt has been downloaded")
        anonFile.close()
    
    if commandLine[0] == 'quit':
        client.send(userCommand.encode(FORMAT))
        print("Exiting Program...")
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        client.close()
        sys.exit()
