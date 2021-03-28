from socket import *

server = "127.0.0.1"
serverPort = 25

#cria socket

socketClient = socket(AF_INET, SOCK_DGRAM)

helo = input("Digite o comando helo + username para iniciar a transação\n")

socketClient.sendto(helo.encode(), (server, serverPort) )

respHelo, addr = socketClient.recvfrom(2048)
if respHelo == "501 Syntax: HELO hostname":
    helo = input("Digite o comando helo + username para iniciar a transação\n")

    socketClient.sendto(helo.encode(), (server, serverPort) )

    respHelo, addr = socketClient.recvfrom(2048)
else:
    print(respHelo)

#

socketClient.close()