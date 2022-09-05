import socket 
import random  
localIP = '127.0.0.1' 
localPort = 8080 
bufferSize = 100 
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
UDPServerSocket.bind((localIP, localPort))  
msgFromServer = 'PONG'  
print('[server] : ready to accept data...')  
while(True):     
	bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     
	message = bytesAddressPair[0]     
	address = bytesAddressPair[1]      
	if random.random() < 0.7:         
		print('[client] : {}'.format(message.decode('utf-8')))         
		bytesToSend = str.encode(msgFromServer)         
		UDPServerSocket.sendto(bytesToSend, address)     
	else:         
		print('[server] : packet dropped') 
