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
    resp, addr = socketServer.recvfrom(2048)
    resposta = resp.decode("UTF-8")
    #se a resposta for o comando certo continua com o processo
    if(resposta == "helo user"):
        resposta = "250 olá user"
        print("realizando envio")
        
        #envia a confirmação 
        socketServer.sendto(resposta.encode(), addr)    
        
        #recebe o email
        rcptMAIL, addr = socketServer.recvfrom(2048)
        mailfro = rcptMAIL.decode("UTF-8")
        a = 0
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
        rcvRCPT.decode("UTF-8")
        b = 0 
        while(b==0):
        #verifica se o remetente esta na lista
            for i in range(len(users)):
                if (rcvRCPT == users[i]):
                    sendRCPT = "250 " + rcvRCPT.decode("UTF-8") + " Recipient OK..."
                    socketServer.sendto(sndEmail.encode(), addr)
                    b = 1;
            if(b==1):
                errorRPCT = "Recipient doesn't exit"
                socketServer.sendto(errorRPCT.encode(), addr)
            
                     
        #recebe o comando DATA
        rcvData, addr = socketServer.recvfrom(2048)
        rcvData.decode("UTF-8")
        # se data == DATA eu continuo o processo
        if(rcvData == "DATA"):
            msgData = "354 Enter mail, end with '.' on a line by itself"
        #não sei oq fazer agr k
        #else:


        
        

    #caso contrario manda uma mensagem de erro
    else:
        resposta = "501 Syntax: HELO hostname"
        print("realizando envio")
        socketServer.sendto(resposta.encode(), addr)    

    
    
    
    
    
socketServer.close()