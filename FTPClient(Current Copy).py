
import socket
import os
import glob
from time import sleep
from math import ceil
from getpass import getpass
import zlib
import zipfile

def main():
    PORT = 12345
    HOST = 'DESKTOP-DLDLEUC'
    s = socket.socket()
    s.connect((HOST, PORT))
    loginAttempts = 0
    while loginAttempts < 3:
        message = s.recv(2048).decode()
        print(message)
        
        username = input("Enter your username: ")
        s.sendall(username.encode())
        
        password = getpass(prompt = "Enter your password: ", stream = None)
        s.send(password.encode())
        
        if '@' not in password:
            print("password must be a propper email address.")
        
        answer = s.recv(2048).decode()
        
        if answer == 'correct':
            print("Successful login attempt!")
            while True:
                string = input("\ninput a string to send: ")
                s.sendall(string.encode())

                if string == 'dir':   
                    x = s.recv(2048).decode()
                    print (x)

                elif string == 'ls':
                    x = s.recv(2048).decode()
                    print(x)

                elif string == 'pwd':
                    x = s.recv(2048).decode()
                    print(x)

                elif string[:4] == 'get ':
                    response = s.recv(2048).decode()
                    print(response + ' bytes')
                    if(response[:4] == 'file'):
                        filename = string[4:]
                        filesize = int(response[27:])
                        packetAmmount = ceil(filesize/2048)
                        if (os.path.isfile('new_' + filename)):
                            x = 1
                            while(os.path.isfile('new_' + str(x) + filename )):
                                x += 1
                            f = open('new_' + str(x) + filename, 'wb')

                        else:
                            f = open("new_" + filename, 'wb')
                        
                        for x in range (0, packetAmmount):
                            data = s.recv(2048)
                            f.write(data)
                        
                        f.close()
                        print("Download is complete")
                    else:
                        print("file does not exist...")
                
                elif string[:4] == 'put ':
                    filename = string[4:]
                    if os.path.isfile(filename):
                        filesize = int(os.path.getsize(filename))
                        s.sendall(('true' + str(filesize)).encode())
                        with open(filename, 'rb') as f:
                            packetAmmount = ceil(filesize/2048)
                            for x in range(0, packetAmmount):
                                bytesToSend = f.read(2048)
                                s.send(bytesToSend)
                        print("file sent!")
                    else:
                        s.sendall('false'.encode())
                        print("file does not exist...")
                
                elif string[:5] == 'mget ':
                    ammountOfFiles = int(s.recv(2048).decode())
                    if ammountOfFiles != 0:
                        for x in range(0, ammountOfFiles):
                            fileName = s.recv(2048).decode()
                            fileSize = s.recv(2048).decode()
                            packetAmmount = ceil(int(fileSize)/2048)
                            if (os.path.isfile('new_' + fileName)):
                                x = 1
                                while(os.path.isfile('new_' + str(x) + fileName)):
                                    x += 1
                                f = open('new_' + str(x) + fileName, 'wb')

                            else:
                                f = open("new_" + fileName, 'wb')
                            
                            for y in range (0, packetAmmount):
                                data = s.recv(2048)
                                f.write(data)
                            
                            f.close()
                        
                        print("download is complete!")
                    else:
                        print("no files are available to download...")
                
                elif string[:5] == 'mput ':
                    filesSent = False
                    if string[5:8] == '*.*':
                        filePath = os.getcwd() + '\\*.*'
                        allFiles = str(glob.glob(filePath))
                        if allFiles != '[]':
                            list = allFiles.split(',')
                            y = 0
                            translation = {39: None, 22: None, 93: None, 91: None}
                            for x in list:
                                filePathList = x.split('\\\\')
                                file = filePathList[-1]
                                file = file.translate(translation)
                                list[y] = file
                                y += 1
                            s.send(str(y).encode())
                            for x in range(0, y):
                                fileSize = os.path.getsize(list[x])
                                sleep(0.1)#this is a delay to make sure that the other computer is actually listening before sending something
                                s.send(str(list[x]).encode())
                                sleep(0.1)#this is a delay to make sure that the other computer is actually listening before sending something
                                s.send(str(fileSize).encode())
                                with open(str(list[x]), 'rb') as f:
                                    packetAmmount = ceil(fileSize/2048)
                                    for z in range(0, packetAmmount):
                                        bytesToSend = f.read(2048)
                                        s.send(bytesToSend)
                            filesSent = True    
                        else:
                            s.send(str(0).encode())


                    elif string[5] == '*':
                        fileExtension = string[6:]
                        filePath = os.getcwd() + '\\*' + fileExtension
                        allFiles = str(glob.glob(filePath))
                        if allFiles != '[]':
                            list = allFiles.split(',')
                            y = 0
                            translation = {39: None, 22: None, 93: None, 91: None}
                            for x in list:
                                filePathList = x.split('\\\\')
                                file = filePathList[-1]
                                file = file.translate(translation)
                                list[y] = file
                                y += 1
                            s.send(str(y).encode())
                            for x in range(0, y):
                                fileSize = os.path.getsize(list[x])
                                sleep(0.1)#this is a delay to make sure that the other computer is actually listening before sending something
                                s.send(str(list[x]).encode())
                                sleep(0.1)#this is a delay to make sure that the other computer is actually listening before sending something
                                s.send(str(fileSize).encode())
                                with open(str(list[x]), 'rb') as f:
                                    packetAmmount = ceil(fileSize/2048)
                                    for z in range(0, packetAmmount):
                                        bytesToSend = f.read(2048)
                                        s.send(bytesToSend)
                            filesSent = True

                        else:
                            s.send(str(0).encode())
                        
                    elif string[-1] == '*':
                        
                        fileName = string[5:-2]
                        filePath = os.getcwd() + '\\' + fileName + '.*'
                        allFiles = str(glob.glob(filePath))
                        if allFiles != '[]':
                            list = allFiles.split(',')
                            y = 0
                            translation = {39: None, 22: None, 93: None, 91: None}
                            for x in list:
                                filePathList = x.split('\\\\')
                                file = filePathList[-1]
                                file = file.translate(translation)
                                list[y] = file
                                y += 1
                            s.send(str(y).encode())
                            for x in range(0, y):
                                fileSize = os.path.getsize(list[x])
                                sleep(0.1)#this is a delay to make sure that the other computer is actually listening before sending something
                                s.send(str(list[x]).encode())
                                sleep(0.1)#this is a delay to make sure that the other computer is actually listening before sending something
                                s.send(str(fileSize).encode())
                                with open(str(list[x]), 'rb') as f:
                                    packetAmmount = ceil(fileSize/2048)
                                    for z in range(0, packetAmmount):
                                        bytesToSend = f.read(2048)
                                        s.send(bytesToSend)
                            filesSent = True
                        
                        else:
                            s.send(str(0).encode())

                    if filesSent:
                        print("Files sent to the server!")
                
                elif string [:9] == 'compress ':
                    x = s.recv(2048).decode()
                    print(x)

                elif string == 'quit':
                    loginAttempts = 4
                    break

        elif answer == 'disconnect':
            break
        loginAttempts += 1
    print("You have been disconnected...")

main()
#https://www.geeksforgeeks.org/getpass-and-getuser-in-python-password-without-echo/

#  (')>  # 
