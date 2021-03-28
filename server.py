from socket import *

serverPort = 25
socketServer = socket(AF_INET, SOCK_DGRAM)

socketServer.bind(("", serverPort))

print("server aguardando...")

while 1:
    
    
    resp, addr = socketServer.recvfrom(2048)
    respota = resp.decode("UTF-8")
    if(respota == "helo user"):
        print("ASDASDA")
        respota = "250 olá user"
    else:
        respota = "501 Syntax: HELO hostname"
    print("realizando envio")
    socketServer.sendto(respota.encode(), addr)


socketServer.close()