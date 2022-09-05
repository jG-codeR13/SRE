import socket  
localIP = '127.0.0.1' 
localPort = 8080 
serverAddressPort = (localIP, localPort) 
bufferSize = 100 
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
UDPClientSocket.settimeout(3)  
msgFromClient = 'PING'  
for i in range(10):     
	byteData = str.encode(msgFromClient)     
UDPClientSocket.sendto(byteData, serverAddressPort)     
try:         
	msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0]         
	print('{} : sent PING... received {}'.format(i+1, msgFromServer))     
except:         
	print('{} : sent PING... Timed Out'.format(i+1)) 
