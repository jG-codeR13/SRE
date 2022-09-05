import socket 
def reverse(string):
    string = string[::-1]
    return string
def rev_sentence(string):
    s = string.split(b' ')[::-1]
    l = []
    for i in s:
    # apending reversed words to l
    	l.append(reverse(i.decode()))
# printing reverse words

    # first split the string into words
    #words = sentence.split(b' ')
 
    # then reverse the split string list and join using space
    reverse_sentence = (" ".join(l))
    return reverse_sentence
    
localIP = '127.0.0.1'
serverPort = 8080 
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverSocket.bind((localIP , serverPort))
print("The server is ready to receive")
while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	modifiedMessage = str.encode(rev_sentence(message))
	serverSocket.sendto(modifiedMessage, clientAddress)
