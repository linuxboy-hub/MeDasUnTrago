from socket	import *
from os import system
from time import sleep
from menu import *
import subprocess   #con el fin de usar subprocess.call(bank2.py)

while True:
    system("clear||cls")
    print (menuClient())
    conn = raw_input("Answer>> ")

    if conn == '0':
        c = socket(AF_INET,SOCK_STREAM)
        c.connect(("localhost",3456))
        while True:
            data = c.recv(1024)
            if data == "thx":
                print("Thanks for your buy")

            elif data == 'nomo':
                print('You do not have the enough money')
                
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
        c.connect(("localhost",1234))
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