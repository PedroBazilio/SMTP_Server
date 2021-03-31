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
    
    #recebe o comando helo
    #se a resposta for o comando certo continua com o processo
    while(1):
        resp, addr = socketServer.recvfrom(2048)
        resposta = resp.decode("UTF-8")
        if(resposta == "helo user"):
            resposta = "250 ola user"
            socketServer.sendto(resposta.encode(), addr) 
            break
        else:
            helERORR = "501 Syntax: HELO hostname"
            socketServer.sendto(helERORR.encode(), addr)   
            
    a = 0
    while(a == 0):
        rcptMAIL, addr = socketServer.recvfrom(2048)
        mailfro = rcptMAIL.decode("UTF-8")
        print(mailfro)
        #lê email do vetor de emails e verifica se existe
        for i in range(len(users)):    
            #se ele existe
            if (mailfro == users[i]):
                a = 1
                sndEmail = "250 " + rcptMAIL.decode("UTF-8") + " Sender OK..."
                socketServer.sendto(sndEmail.encode(), addr)
                
        #caso o email n exista na lista
        if(a == 0):
            erroSender = "Email inexistente, tente novamente"
            socketServer.sendto(erroSender.encode(), addr)    
            

    #recebe os dados do remetente
    
    b = 0 
    while(b == 0):
    #verifica se o remetente esta na lista
        rcvRCPT, addr = socketServer.recvfrom(2048)
        rcvRCP = rcvRCPT.decode("UTF-8")
        for i in range(len(users)):
            if (rcvRCP == users[i]):
                sendRCPT = "250 " + rcvRCPT.decode("UTF-8") + " Recipient OK..."
                socketServer.sendto(sendRCPT.encode(), addr)
                b = 1;
                
        if(b==0):
            errorRPCT = "Recipient doesn't exit"
            socketServer.sendto(errorRPCT.encode(), addr)

    print(rcvRCP)
            
                    
    #recebe o comando DATA
    # se data == DATA eu continuo o processo
    while(1):
        rcvData, addr = socketServer.recvfrom(2048)
        rcvDAT = rcvData.decode("UTF-8")
        if(rcvDAT == "DATA"):
            msgData = "354 Enter mail, end with '.' on a line by itself"
            socketServer.sendto(msgData.encode(), addr)
            break
        else:
            msgData = "500 Syntax error, command unrecognized"
            socketServer.sendto(msgData.encode(), addr)

    print("Esperando mensagem do remetente.\n")
        
    #recebe a mensagem email 
    listMail = []
    rcvMail, addr = socketServer.recvfrom(4096)
    rcvMai = rcvMail.decode("UTF-8")
    listMail.append(rcvMai)
    w = 0
    while(w == 0):
        rcvMail, addr = socketServer.recvfrom(4096)
        rcvMai = rcvMail.decode("UTF-8")
        if(rcvMai != "."):
            listMail.append(rcvMai)
        else:
            w = 1

    for i in range (len(listMail)):
        print(listMail[i])
    
    
    
    
    msgMail = "250 Message accepted for delivery"
    socketServer.sendto(msgMail.encode(), addr)


    
    
    
    
socketServer.close()