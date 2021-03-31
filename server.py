from socket import *
import os

serverPort = 25
socketServer = socket(AF_INET, SOCK_DGRAM)

socketServer.bind(("", serverPort))

print("aguardando arquivo de usuarios")
#poe os usuarios em uma lista
rcvUsers, addr = socketServer.recvfrom(2048)
rcvUser = rcvUsers.decode("UTF-8")

users = list()        
try:
    with open (str(rcvUser)+".txt", "r") as user:
        for line in user:
            users.append(line.strip());
        print("Arquivo recebido com sucesso")
    #faz uma caixa de entrada para cada usuario

    for i in range(len(users)):
        user = users[i]
        file = open(str(user)+".txt","w");
        file.close();

    msgSuc = "Arquivo aberto com sucesso"
    socketServer.sendto(msgSuc.encode(), addr)


except IOError:

    msgError = "Arquivo inexistente"
    socketServer.sendto(msgError.encode(), addr)
    aux = 1

print("server aguardando...")

aux = 0
while (aux == 0):
    aux2 = 0
    #recebe o comando helo
    #se a resposta for o comando certo continua com o processo
    while(aux2 == 0):
        resp, addr = socketServer.recvfrom(2048)
        resposta = resp.decode("UTF-8")
        
        if(resposta == "QUIT"):
            aux2 = 1
            socketServer.sendto(resposta.encode(), addr)
            break
    
        
        if(resposta == "HELO user"):
            resposta = "250 Ola user"
            socketServer.sendto(resposta.encode(), addr) 
            break
        else:
            helERORR = "500 Syntax error, command unrecognized"
            socketServer.sendto(helERORR.encode(), addr)   

    if(aux2==1):
        print("Codigo encerrado")
        break
    
    
    
    a = 0
    while(a == 0):
        rcptMAIL, addr = socketServer.recvfrom(2048)
        mailfro = rcptMAIL.decode("UTF-8")
        
        if (mailfro == "QUIT"):
            a = 2
            socketServer.sendto(mailfro.encode(), addr)
            break
        
        #lê email do vetor de emails e verifica se existe
        for i in range(len(users)):    
            #se ele existe
            if (mailfro == users[i]):
                a = 1
                sndEmail = "250 " + rcptMAIL.decode("UTF-8") + " Sender OK..."
                socketServer.sendto(sndEmail.encode(), addr)
                
        #caso o email n exista na lista
        if(a == 0):
            erroSender = "550 Address Unkonown"
            socketServer.sendto(erroSender.encode(), addr)    
    
    
    if(a==2):
        print("Codigo encerrado")
        break
           
    print("Mail From: " + mailfro)

    #recebe os dados do remetente
    
    b = 0 
    while(b == 0):
    #verifica se o remetente esta na lista
        rcvRCPT, addr = socketServer.recvfrom(2048)
        rcvRCP = rcvRCPT.decode("UTF-8")
        if(rcvRCP == "QUIT"):
            b = 2
            socketServer.sendto(rcvRCP.encode(), addr)
            break
        
        for i in range(len(users)):
            if (rcvRCP == users[i]):
                sendRCPT = "250 " + rcvRCPT.decode("UTF-8") + " Recipient OK..."
                socketServer.sendto(sendRCPT.encode(), addr)
                b = 1;
                
        if(b==0):
            errorRPCT = "550 Address Unkonown"
            socketServer.sendto(errorRPCT.encode(), addr)
    
    if(b==2):
        print("Codigo encerrado")
        break

    print("RCPT TO: " + rcvRCP)
    print("\n")
            
                    
    #recebe o comando DATA
    # se data == DATA eu continuo o processo
    while(1):
        rcvData, addr = socketServer.recvfrom(2048)
        rcvDAT = rcvData.decode("UTF-8")
        if(rcvDAT == "QUIT"):
            aux2 = 1
            socketServer.sendto(rcvDAT.encode(), addr)
            break
        
        if(rcvDAT == "DATA"):
            msgData = "354 Enter mail, end with '.' on a line by itself"
            socketServer.sendto(msgData.encode(), addr)
            break
        else:
            msgData = "500 Syntax error, command unrecognized"
            socketServer.sendto(msgData.encode(), addr)
    
    if(aux2==1):
        print("Codigo encerrado")
        break
    #print("Esperando mensagem do remetente.\n")
        
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
    
    for i in range(len(users)):
        if(rcvRCP == users[i]):
            file = open(str(rcvRCP)+".txt","a+");
            file.write("Mail From: "+ mailfro + "\n")
            for i in range(len(listMail)):
                file.write(listMail[i]+ "\n")
            file.write("\n\n")
            file.close();
    
    
    msgMail = "250 Message accepted for delivery"
    socketServer.sendto(msgMail.encode(), addr)
    print("\n")

    
    
    
    
socketServer.close()