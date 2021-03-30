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
    z = 0
    while(z==0):
        resp, addr = socketServer.recvfrom(2048)
        resposta = resp.decode("UTF-8")
        if(resposta == "helo user"):
            resposta = "250 ola user"
            socketServer.sendto(resposta.encode(), addr) 
            z=1  
        if(z==0):
            helERORR = "501 Syntax: HELO hostname"
            socketServer.sendto(helERORR.encode(), addr)   
            
    a = 0
    rcptMAIL, addr = socketServer.recvfrom(2048)
    mailfro = rcptMAIL.decode("UTF-8")
    while(a == 0):
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
    
    rcvRCPT, addr = socketServer.recvfrom(2048)
    rcvRCP = rcvRCPT.decode("UTF-8")
    b = 0 
    while(b==0):
    #verifica se o remetente esta na lista
        for i in range(len(users)):
            if (rcvRCP == users[i]):
                sendRCPT = "250 " + rcvRCPT.decode("UTF-8") + " Recipient OK..."
                socketServer.sendto(sendRCPT.encode(), addr)
            
                b = 1;
        if(b==0):
            errorRPCT = "Recipient doesn't exit"
            socketServer.sendto(errorRPCT.encode(), addr)
            
                    
    #recebe o comando DATA
    rcvData, addr = socketServer.recvfrom(2048)
    rcvDAT = rcvData.decode("UTF-8")
    # se data == DATA eu continuo o processo
    c = 0
    while(c == 0):
        if(rcvDAT == "DATA"):
            msgData = "354 Enter mail, end with '.' on a line by itself"
            socketServer.sendto(msgData.encode(), addr)
            
            c = 1
        if(c==0):
            msgData = "500 Syntax error, command unrecognized"
            socketServer.sendto(msgData.encode(), addr)
        
    #recebe o email 
    rcvMail, addr = socketServer.recvfrom(4096)
    rcvMai = rcvMail.decode("UTF-8")
    print(rcvMai)
    msgMail = "250 Message accepted for delivery"
    socketServer.sendto(msgMail.encode(), addr)


    
    
    

#caso contrario manda uma mensagem de erro
else:
    resposta = "501 Syntax: HELO hostname"
    print("realizando envio")
    socketServer.sendto(resposta.encode(), addr)    

    
    
    
    
    
socketServer.close()