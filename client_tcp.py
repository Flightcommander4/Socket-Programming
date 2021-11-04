# Matthew Calandrella - ECE 416 Assignment #1 (Client TCP)

#Importing Libraries
import socket
import sys

#Defining Variables and Other Useful Information
HEADER = 64
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
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

#Creating a new Socket, and Defining the Method of Streaming the Data, as well as Connecting the Client to the defined Server and Port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#Defining sending a message to the server, and receiving a message from the server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

while True:

    #Asks the user for a command, and determines what the user will be doing
    command = input(str("Enter Command: "))
    commandLine = command.split(" ")
    userCommand = commandLine[0]
    print('Awaiting Server Response')
    
    #If the user enters put, this code executes and uploads the given file to the Server
    if commandLine[0] == 'put':
        client.send(userCommand.encode(FORMAT))
        filename = commandLine [1]
        file = open(filename, 'rb')
        fileread = file.read()
        while(fileread):
            print("Sending file...")
            client.send(fileread)
            fileread = file.read()
        file.close()
        print("Done Sending")

    #If the user enters keyword, the given keyword to be anonymized by the server, however the file they enter
    #must be the same as the file uploaded previously, or else an error will occur
    if commandLine[0] == 'keyword':
        client.send(userCommand.encode(FORMAT))
        keyword = commandLine[1]
        client.send(keyword.encode(FORMAT))
        keywordMsg = client.recv(10000).decode(FORMAT)
        
        #When the Keyword is Received, we will prepare the file for download
        if keywordMsg == 'Keyword Received':
            file = open(filename, 'rb')
            fileread = file.read()
            while(fileread):
                client.send(fileread)
                fileread = file.read()
            file.close()
            newFile = filename.split(".")
            print(f'Server Response: {filename} has been anonymized, Output is {newFile[0]}_anon.txt')
    

    #The "get" command will download the newly created anonymized file in the same directory as the 
    #client_tcp.py file
    if commandLine[0] == 'get':
        client.send(userCommand.encode(FORMAT))
        newFile = filename.split(".")
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
        sys.exit()
