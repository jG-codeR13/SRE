import socket
localIP = '127.0.0.1'
serverPort = 8080 
clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
msg = input('Input lowercase sentence:')
byteData = str.encode(msg)     
#UDPClientSocket.sendto( serverAddressPort) 
clientSocket.sendto(byteData,(localIP,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()
