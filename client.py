from socket	import *
from os import system
from time import sleep
from menu import *
liquorIp = "127.0.0.1"
bankIp = "127.0.0.1"

while True:
    system("clear||cls")
    print (menuClient())
    conn = raw_input("Answer>> ")

    if conn == '0':
        c = socket(AF_INET,SOCK_STREAM)
        c.connect((liquorIp,3456))
        while True:
            data = c.recv(1024)
            if (data == "thx" or data == 'inf'):
                data = c.recv(1024)
                print data
                
            elif data == "bye":
                print ("Have a nice day, bye...")
                sleep(1)
                system("clear||cls")
                break
            
            else:
                system("clear||cls")
                print data
                request= raw_input("\nAnswer >> ")
                c.send(request)
        c.close()

    elif conn == '1':
        c = socket(AF_INET,SOCK_STREAM)
        c.connect((bankIp,1234))
        while True:
            data = c.recv(1024)
            if data == "bye":
                print ("Have a nice day, bye...")
                sleep(1)
                system("clear||cls")
                break

            elif (data == 'inf'or data == 'err'):
                data = c.recv(1024)
                print data

            else:
                system("clear||cls")
                print data
                request= raw_input("\nAnswer >> ")
                c.send(request)
        c.close()
    else:
        system("clear||cls")
        exit()
