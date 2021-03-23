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

