import socket
import sys
import os
import select
import random
import datetime
import time
from itertools import cycle

#Define a constant for the buffer size
BUFFER_SIZE = 1024

#Define a constant for how many minutes the balancer should run until it times out
MINUTES = 1
SERVER_POOL = [('10.0.2.15', 8888),('10.0.2.15', 8080)]
# A function that creates an HTTP header
def createHeader(sock):
    message = 'HTTP/1.1 301 Moved Permanently \r\nLocation: '+str(sock.getpeername()[0])+':'+str(sock.getpeername()[1])+' \r\n\r\n'
    return message


# A function to create a HTTP GET message
def createGetMessage(ip, port, fileName):
    request = f'GET {fileName} HTTP/1.1\r\nHost: {ip}:{port}\r\n\r\n'
    return request

class loadBalancer(object):
    socketList = list()
    timeout = time.time() + 60*MINUTES

    def __init__(self):
        self.ip = 'localhost'
        self.port = 0
        self.clientSocket =socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientSocket.bind((self.ip, int(self.port)))
        self.clientSocket.listen(10)
        print("Balancer's address and port:", self.clientSocket.getsockname())

    # Function used to redirect client to the server
    def start(self):
    	while True:
            print("Balancer is listening...")
            if time.time() > self.timeout:
                print("Reconfiguring servers...")
                self.timeout = time.time() + 60*MINUTES
                self.setup()
                self.start()
            try:
                connection, addr = self.clientSocket.accept()
                print("Got connection from", addr)
                serverSocket = self.select()
                request = connection.recv(BUFFER_SIZE).decode()
                message = createHeader(serverSocket)
                connection.send(message.encode())
            except socket.error:
                #If a server crashes, remove it from the list
                self.setup()
    def on_accept(self):
    	client_socket, client_addr = self.cs_socket.accept()
        print 'client connected: %s <==> %s' % (client_addr, self.cs_socket.getsockname())

        # select a server that forwards packets to
        server_ip, server_port = self.select_server(SERVER_POOL, self.algorithm)

        # init a server-side socket
        ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ss_socket.connect((server_ip, server_port))
            print 'init server-side socket: %s' % (ss_socket.getsockname(),)
            print 'server connected: %s <==> %s' % (ss_socket.getsockname(),(socket.gethostbyname(server_ip), server_port))
        except:
            print "Can't establish connection with remote server, err: %s" % sys.exc_info()[0]
            print "Closing connection with client socket %s" % (client_addr,)
            client_socket.close()
            return

        self.sockets.append(client_socket)
        self.sockets.append(ss_socket)

        self.flow_table[client_socket] = ss_socket
        self.flow_table[ss_socket] = client_socket

    def on_recv(self, sock, data):
        print 'recving packets: %-20s ==> %-20s, data: %s' % (sock.getpeername(), sock.getsockname(), [data])
        # data can be modified before forwarding to server
        # lots of add-on features can be added here
        remote_socket = self.flow_table[sock]
        remote_socket.send(data)
        print 'sending packets: %-20s ==> %-20s, data: %s' % (remote_socket.getsockname(), remote_socket.getpeername(), [data])

    def on_close(self, sock):
        print 'client %s has disconnected' % (sock.getpeername(),)
        print '='*41+'flow end'+'='*40

        ss_socket = self.flow_table[sock]

        self.sockets.remove(sock)
        self.sockets.remove(ss_socket)

        sock.close()  # close connection with client
        ss_socket.close()  # close connection with server

        del self.flow_table[sock]
        del self.flow_table[ss_socket]

    def select_server(self, server_list, algorithm):
        if algorithm == 'random':
            return random.choice(server_list)
        elif algorithm == 'round robin':
            return round_robin(ITER)
        else:
            raise Exception('unknown algorithm: %s' % algorithm)


if __name__ == '__main__':
    try:
        LoadBalancer('localhost', 5555, 'round robin').start()
    except KeyboardInterrupt:
        print "Ctrl C - Stopping load_balancer"
        sys.exit(1)  
    # Function used to configure the server sockets and pick a socket to use for the client
    '''def setup(self):
        compList = []
        self.socketList.clear()
        if len(sys.argv) <= 1:
            print("Please enter servers in the command line!")
            sys.exit(1)
        print("Available servers:")
        #Runs performance test
        for i in range(0, len(sys.argv)-1):
            try:
                serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
                splitAddress = sys.argv[i+1].split(":")
                serverIP = splitAddress[0]
                serverPort = splitAddress[1]
                serverSocket.connect((serverIP, int(serverPort)))
                message = createGetMessage(serverIP, serverPort, 'test.txt')
                startTime = datetime.datetime.now()
                serverSocket.send(message.encode())
                while True:
                    received = serverSocket.recv(BUFFER_SIZE)
                    if not received:
                        break
                endTime = datetime.datetime.now()
                totalTime = (endTime - startTime).microseconds
                compList.append(totalTime)
                self.socketList.append(serverSocket)
                print(serverSocket.getpeername())
            except:
                print("('" + serverIP + "', "+serverPort+") is not available.")

        if len(compList) == 0:
            print("There are no servers remaining!")
            sys.exit(1)

        #Increases the chance of using a faster socket by appending more faster sockets
        for i in range(0, len(compList)):
            for j in range(0, len(compList)):
                if j > i:
                    self.socketList.append(self.socketList[j])

    def select(self):
    
        return random.choice(self.socketList)

if __name__ == '__main__':
    try:
        balancer = loadBalancer()
        balancer.setup()
        balancer.start()
    except KeyboardInterrupt:
        print("Interrupt detected! Exiting the balancer...")
        sys.exit(1)'''
        

