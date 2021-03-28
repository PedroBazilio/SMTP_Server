from socket import *
import os

#poe os usuarios em uma lista

users = list()        
with open ("NomesDeUsuarios.txt", "r") as user:
    for line in user:
        users.append(line.strip());



#faz uma caixa de entrada para cada usuario

for i in range(len(users)):
    user = users[i]
    file = open(str(user)+".txt","w");
    file.close();


serverPort = 25
socketServer = socket(AF_INET, SOCK_DGRAM)

socketServer.bind(("", serverPort))

print("server aguardando...")

while 1:
    
    
    resp, addr = socketServer.recvfrom(2048)
    resposta = resp.decode("UTF-8")
    if(resposta == "helo user"):
        resposta = "250 olá user"
        print("realizando envio")
        socketServer.sendto(resposta.encode(), addr)    
        mailfrom, addr = socketServer.recvfrom(2048)
        mailfro = mailfrom.decode("UTF-8")
        a = 0
        while(a = 0):
            for i in range(len(users)):    
                if (mailfro == users[i]):
                    a = 1
                    socketServer.sendto(mailfro.encode(), addr)
            if(a = 0):
                
        


    else:
        resposta = "501 Syntax: HELO hostname"
    

    
    
    
    
    
socketServer.close()