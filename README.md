# FTP-server-Project
This is the project that was assigned in my csc 311 Networking class. The goal was to create a successful file server which connects two computers together via sockets and allows for there to be an ftp server waiting for a connection and an ftp client who is connecting to the server. This project was done in python using the python socket library. In order for you to get this to work you must have the server program being run on a separtate computer with an ethernet connecting the other computer which is running the client. The client will then be able to navigate through the filesystem on the server computer and select a file  to download.

These two programs are designed to work together as a client and server pair. The server program is to be started on another computer to have it start listening for a connection. The client computer is to then connect to the computer with the server on it via a lan cable. Once they connect the computer running the client program can communicate to the server program on the server computer.

The client program must first try to login to the server with a correct username and password that can be found saved in the server computer as two string varables. The client has three attempts to answer with the correct username and password or else it gets kicked off and it must try to reconnect again.

The client computer can navigate through the filesystem of the server computer and list out all of the files and directories on the computer that the server program is being run on.

# Commands that can be run from the client computer:

 - cd
 change directory
 
 - ls
 Linux list directory – files and directories listed together in alphabetic order

 - dir
 Windows list directory – directories first in alphabetic order followed by files in alphabetic order

 - get
  get “file” from server
  *Files that are larger are transfered in chunks of 2048 bits.*

 - put
  put “file” from client to server
  *Files that are larger are transfered in chunks of 2048 bits.*

 - mget
  get multiple files from server with “name.*” or “*.ext” or “*.*” (all)

 - mput
  put multiple files from client to server with “name.*” or “*.ext” or “*.*” (all)

 - compress
  compress a file on the server side so it can be smaller for when you want to 'get' the file
