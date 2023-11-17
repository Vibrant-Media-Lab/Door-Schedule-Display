import socket
from webscrape import scrape
s=socket.socket()

port=1234

s.connect(('136.142.159.51', port)) # IP address of server will need to replace this with your servers IP address

print(s.recv(1024))

scan = scrape()
print(scan)

# this does not work currently. If you decide to go this route of making the raspberry pi a server and running a seperate client 
# you will need to change this. I feel like the idea was there but I'm not sure how to package the strings/encode them to send to the server.
# But honestly theres no reason why you should need a client and server when the raspberry pi can simply connect to the internet it's self and
# scrape the information and send it to the display without having to go through a client. 
for i in scan:
    String = str(i)
    print(String + " Sending")
    s.send(String.encode())
    print(s.recv(1024))

s.send(b'Bye')

s.close()