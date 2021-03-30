from socket import *

server = "127.0.0.1"
serverPort = 25

#cria socket

socketClient = socket(AF_INET, SOCK_DGRAM)
while 1:
    #envio do helo

    helo = input("Digite o comando helo + username para iniciar a transação\n")
    socketClient.sendto(helo.encode(), (server, serverPort) )
    respHelo, addr = socketClient.recvfrom(2048)
    respHel = respHelo.decode("UTF-8")
    
    #caso helo receba um erro, pede para repetir o processp    
    if respHel == "501 Syntax: HELO hostname":
        helo = input("Digite o comando helo + username para iniciar a transação\n")

        socketClient.sendto(helo.encode(), (server, serverPort) )

        respHelo, addr = socketClient.recvfrom(2048)
    #caso contrario, continua o processo
    else:
        print(respHel)
        print("\n")
        
        #recebe o email e faz o envio para o servidor
        mailFrom = input("Mail From: ")
        #envia email para o servidor
        socketClient.sendto(mailFrom.encode(), (server, serverPort))               
        respMailFrom, addr = socketClient.recvfrom(2048)
        respMailFro = respMailFrom.decode("UTF-8")
        #se a resposta for um email que não existe pede para repetir o processo
        
        if(respMailFro == "Email inexistente, tente novamente"):
            print(respMailFro)
            mailFrom = input("Mail From: ")
            socketClient.sendto(mailFrom.encode(), (server, serverPort))               
            respMailFrom, addr = socketClient.recvfrom(2048)
            respMailFro = respMailFrom.decode("UTF-8")
        #caso contrario continua o processo
        else:
            print(respMailFro)
            sndRCPT = input("RCPT TO: ")
            socketClient.sendto(sndRCPT.encode(), server, serverPort)
            rcvRCPT, addr = socketClient.recvfrom(2048)            
            rcvRCPT.decode("UTF-8")
            #o remetente nao existe
            if(rcvRCPT == "Recipient doesn't exit"):
                sndRCPT = input("RCPT TO: ")
                socketClient.sendto(sndRCPT.encode(), server, serverPort)
                rcvRCPT, addr = socketClient.recvfrom(2048)            
                rcvRCPT.decode("UTF-8")
            # o remetente existe
            else:
                print(rcvRCPT)
                #Recebe Data
                sndDATA = input()
                socketClient.sendto(sndDATA.encode(), server, serverPort)
                rcvDATA, addr = socketClient.recvfrom(2048)
                rcvDATA.decode("UTF-8")
                if(rcvDATA == "mensagem de erro"):
                
                #else:

            
            
            
            # #recebe DATA do user
            # data = input()
            # socketClient.sendto(data.encode(), (server, serverPort))


socketClient.close()