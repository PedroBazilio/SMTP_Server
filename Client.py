from socket import *

server = "127.0.0.1"
serverPort = 25

#cria socket
socketClient = socket(AF_INET, SOCK_DGRAM)

usuarios = input("Digite o arquivo de usuarios a ser lido: ")
socketClient.sendto(usuarios.encode(), (server, serverPort))
msgUsers, addr = socketClient.recvfrom(2048)
msgUser = msgUsers.decode("UTF-8")



if(msgUser == "Arquivo aberto com sucesso"):
    print(msgUser)
    while 1:
        aux3 = 0
        #envio do helo
        helo = input("Digite o comando HELO + username para iniciar a transação\n")
        socketClient.sendto(helo.encode(), (server, serverPort))
        respHelo, addr = socketClient.recvfrom(2048)
        respHel = respHelo.decode("UTF-8")
        if(respHel == "QUIT"):
            break
        while(respHel == "500 Syntax error, command unrecognized"):
        #caso helo receba um erro, pede para repetir o processp    
            print(respHel)
            helo = input("Digite o comando HELO + user para iniciar a transação\n")
            socketClient.sendto(helo.encode(), (server, serverPort) )
            respHelo, addr = socketClient.recvfrom(2048)
            respHel = respHelo.decode("UTF-8")
            if(respHel == "QUIT"):
                aux3 = 1
                break
        if(aux3 == 1):
            break

        print(respHel)
        
        
        #recebe o email e faz o envio para o servidor
        mailFrom = input("Mail From: ")
        #envia email para o servidor
        socketClient.sendto(mailFrom.encode(), (server, serverPort))               
        respMailFrom, addr = socketClient.recvfrom(2048)
        respMailFro = respMailFrom.decode("UTF-8")
        if(respMailFro == "QUIT"):
            break
        #se a resposta for um email que não existe pede para repetir o processo
        while(respMailFro == "550 Address Unkonown"):
            print(respMailFro)
            mailFrom = input("Mail From: ")
            socketClient.sendto(mailFrom.encode(), (server, serverPort))               
            respMailFrom, addr = socketClient.recvfrom(2048)
            respMailFro = respMailFrom.decode("UTF-8")
            if(respMailFro == "QUIT"):
                aux3 = 1
                break
         
        if(aux3 == 1):
            break
            
        print(respMailFro)
        sndRCPT = input("RCPT TO: ")
        socketClient.sendto(sndRCPT.encode(), (server, serverPort))
        rcvRCPT, addr = socketClient.recvfrom(2048)            
        rcvRCP = rcvRCPT.decode("UTF-8")
        if(rcvRCP == "QUIT"):
            break
        
        
        
        #o remetente nao existe
        while(rcvRCP == "550 Address Unkonown"):
            print(rcvRCP)
            sndRCPT = input("RCPT TO: ")
            socketClient.sendto(sndRCPT.encode(), (server, serverPort))
            rcvRCPT, addr = socketClient.recvfrom(2048)            
            rcvRCP = rcvRCPT.decode("UTF-8")
            if(rcvRCP == "QUIT"):
                aux3 = 1 
                break
        if(aux3 == 1):
            break

        print(rcvRCP)
        
        
        
        #Recebe Data
        sndDATA = input()
        socketClient.sendto(sndDATA.encode(), (server, serverPort))
        rcvDATA, addr = socketClient.recvfrom(2048)
        rcvDAT = rcvDATA.decode("UTF-8")
        if(rcvDAT == "QUIT"):    
            break
        
        while(rcvDAT == "500 Syntax error, command unrecognized"):
            print(rcvDAT)
            sndDATA = input()
            socketClient.sendto(sndDATA.encode(), (server, serverPort))
            rcvDATA, addr = socketClient.recvfrom(2048)
            rcvDAT = rcvDATA.decode("UTF-8")
            if(rcvDAT == "QUIT"):
                aux3 = 1
                break
        
        if(aux3 == 1):
            break
        print(rcvDAT)
        
        listEmail = []
        while(1):#recebe a mensagem do email
            email = input()
            if(email == "."):
                listEmail.append(email)  
                break
            else:
                listEmail.append(email)
        for i in range (len(listEmail)):
            socketClient.sendto(listEmail[i].encode(), (server, serverPort))
        msgEmail, addr =  socketClient.recvfrom(2048)
        msg = msgEmail.decode("UTF-8")
        print(msg)
else:
    print(msgUser)
    
    

socketClient.close()
