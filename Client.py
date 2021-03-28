from socket import *

server = "127.0.0.1"
serverPort = 25

#cria socket

socketClient = socket(AF_INET, SOCK_DGRAM)
while 1:
    helo = input("Digite o comando helo + username para iniciar a transação\n")

    socketClient.sendto(helo.encode(), (server, serverPort) )

    respHelo, addr = socketClient.recvfrom(2048)
    respHel = respHelo.decode("UTF-8")
    if respHel == "501 Syntax: HELO hostname":
        helo = input("Digite o comando helo + username para iniciar a transação\n")

        socketClient.sendto(helo.encode(), (server, serverPort) )

        respHelo, addr = socketClient.recvfrom(2048)
    else:
        print(respHel)
        print("\n")
        mailFrom = input("Mail From: ")
        socketClient.sendto(mailFrom.encode(), (server, serverPort))               
        respMailFrom, addr = socketClient.recvfrom(2048)
        respMailFro = respMailFrom.decode("UTF-8")
        if(respMailFro == "")
    
    #

socketClient.close()