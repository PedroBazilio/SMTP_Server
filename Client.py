from socket import *

server = "127.0.0.1"
serverPort = 25

#cria socket

socketClient = socket(AF_INET, SOCK_DGRAM)
while 1:
    #envio do helo
    q = 0
    
    helo = input("Digite o comando helo + username para iniciar a transação\n")
    socketClient.sendto(helo.encode(), (server, serverPort))
    respHelo, addr = socketClient.recvfrom(2048)
    respHel = respHelo.decode("UTF-8")
    while(respHel == "501 Syntax: HELO hostname"):
    #caso helo receba um erro, pede para repetir o processp    
        print(respHel)
        helo = input("Digite o comando helo + username para iniciar a transação\n")
        socketClient.sendto(helo.encode(), (server, serverPort) )
        respHelo, addr = socketClient.recvfrom(2048)
        respHel = respHelo.decode("UTF-8")
        
    
    print(respHel)
    print("\n")
    
    #recebe o email e faz o envio para o servidor
    mailFrom = input("Mail From: ")
    #envia email para o servidor
    socketClient.sendto(mailFrom.encode(), (server, serverPort))               
    respMailFrom, addr = socketClient.recvfrom(2048)
    respMailFro = respMailFrom.decode("UTF-8")
    
    #se a resposta for um email que não existe pede para repetir o processo
    while(respMailFro == "Email inexistente, tente novamente"):
        print(respMailFro)
        mailFrom = input("Mail From: ")
        socketClient.sendto(mailFrom.encode(), (server, serverPort))               
        respMailFrom, addr = socketClient.recvfrom(2048)
        respMailFro = respMailFrom.decode("UTF-8")
        
        
    print(respMailFro)
    sndRCPT = input("RCPT TO: ")
    socketClient.sendto(sndRCPT.encode(), (server, serverPort))
    rcvRCPT, addr = socketClient.recvfrom(2048)            
    rcvRCPT.decode("UTF-8")
    #o remetente nao existe
    while(rcvRCPT == "Recipient doesn't exit"):
        sndRCPT = input("RCPT TO: ")
        socketClient.sendto(sndRCPT.encode(), (server, serverPort))
        rcvRCPT, addr = socketClient.recvfrom(2048)            
        rcvRCPT.decode("UTF-8")


    print(rcvRCPT)
    #Recebe Data
    sndDATA = input()
    socketClient.sendto(sndDATA.encode(), (server, serverPort))
    rcvDATA, addr = socketClient.recvfrom(2048)
    rcvDATA.decode("UTF-8")
    while(rcvDATA == "inserir codigo de erro"):
        print(rcvDATA)
        sndDATA = input()
        socketClient.sendto(sndDATA.encode(), (server, serverPort))
        rcvDATA, addr = socketClient.recvfrom(2048)
        rcvDATA.decode("UTF-8")
    
    print(rcvDATA)
    listEmail = []
    a = 0
    while(a==0):
        email = input()
        if(email == "."):
            a=1       
        else:
            listEmail.append(email)
    for i in range (len(listEmail)):
        socketClient.sendto(listEmail[i].encode(), (server, serverPort))
    msgEmail, addr =  socketClient.recvfrom(2048)
    msgEmail.decode("UTF-8")
    print(msgEmail)

    
    

socketClient.close()

#desculpa professor :_(