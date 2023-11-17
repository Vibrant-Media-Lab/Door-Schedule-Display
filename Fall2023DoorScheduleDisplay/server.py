
import socket
 
s = socket.socket()
print("Socket successfully created")

port = 1234

s.bind(('', port))
print("socket binded to %s" %(port))

s.listen(5)
print("Socket is listening...")

while True:       
    # Establish connection with client.
    c, addr = s.accept()
    
    print ('Got connection from', addr )
    # send a thank you message to the client.
    
    c.send(b'Thank you for connecting to the server!')
    # Receive data from the client
    
    # My idea here was an infinite loop that will recive data from the client and send a message back to the client signaling that it's ready for
    # more
    while True:
        print(c.recv(1024))
        c.send(b'done')
        if c.recv(1024) == b'Bye':
            break
    # Close the connection with the client
    c.close()
    