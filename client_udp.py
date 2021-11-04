# Matthew Calandrella - ECE 416 Assignment #1 (Client UDP)

#Importing Libraries
import socket
import sys

#Defining Variables and Other Useful Information
HEADER = 64
SERVER = (sys.argv[1])
PORT = int(sys.argv[2])
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


#************************************************************************************************************************************
#  Stack Overflow Links Used for Guidance:
#  Reading in Binary: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
#  Error Help: https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
#  UDP Help: https://stackoverflow.com/questions/27893804/udp-client-server-socket-in-python
#  TCP Help: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
#************************************************************************************************************************************

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((SERVER, PORT))

#print("Ready to Send Data")
#client.sendto(bytes(input(), FORMAT), (SERVER, PORT))
#newMsg, serverAddress = client.recvfrom(1024)
#print(newMsg.decode(FORMAT) + ' from ' + str(serverAddress))

while True:

    command = input(str("Enter Command: "))
    commandLine = command.split(" ")
    userCommand = commandLine[0]
    print('Awaiting Server Response')

    #If the user enters put, this code executes and uploads the given file to the Server
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
            fileRead = fileOpen.read(1000)
            print(f'Length of Chunks will be: {len(fileRead)}')
            
            #Checking if the FIle is done being read with each loop iteration
            while fileRead != b"":
                client.sendto(fileRead, (ADDR))
                ackMsg, serverAddress = client.recvfrom(1024)
                print(ackMsg.decode(FORMAT))
                fileRead = fileOpen.read(1000)
                client.sendto(fileRead, (ADDR))
                
        print('Done Sending File')

    #If the user enters keyword, the given keyword to be anonymized by the server, however the file they enter
    #must be the same as the file uploaded previously, or else an error will occur
    if commandLine[0] == 'keyword':
        client.sendto(userCommand.encode(FORMAT), ADDR)
        keyword = commandLine[1]
        keywordFile = commandLine[2]
        client.send(keyword.encode(FORMAT))
        keywordMsg, serverAddress = client.recvfrom(10000)
        keywordMsg = keywordMsg.decode(FORMAT)
        
        #When the Keyword is Received, we will prepare the file for download
        if keywordMsg == 'Keyword Received':
            file = open(keywordFile, 'rb')
            fileread = file.read()
            while(fileread):
                client.send(fileread)
                fileread = file.read()
            file.close()
            newFile = keywordFile.split(".")
            print(f'Server Response: {keywordFile} has been anonymized, Output is {newFile[0]}_anon.txt')
    
    #The "get" command will download the newly created anonymized file in the same directory as the 
    #client_tcp.py file
    if commandLine[0] == 'get':
        client.send(userCommand.encode(FORMAT))
        newFile = keywordFile.split(".")
        newAnonText = client.recv(100000).decode(FORMAT)
        newAnonFile = open(newFile[0] + "_anon.txt", 'w')
        newAnonFile.write(newAnonText)
        print(f"File {newFile[0]}_anon.txt has been downloaded")
        newAnonFile.close()

    #This command will quit the program and send a disconnect msg to the server, letting the
    #server know the user has disconnected
    if commandLine[0] == 'quit':
        client.send(userCommand.encode(FORMAT))
        print("Exiting Program...")
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        client.close()
        sys.exit()
