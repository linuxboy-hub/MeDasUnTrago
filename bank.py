from SocketServer import ThreadingUDPServer, ThreadingTCPServer, BaseRequestHandler
from threading import Thread
from menu import *
from os import system
from time import sleep
from cesar import *
from random import randint

system("clear||cls")
print "Bank is open!"
accounts = {'000':{'name': 'Mateo Jaramillo', 'password':'mateo123', 'balance':318890, 'dyn':0},
    '001':{'name': 'Daniela Jurado', 'password':'daniela123', 'balance':3200000,'dyn':0},
    '002':{'name': 'Luis Carlos', 'password':'carlos789', 'balance':300000,'dyn':0}
}
bankIp = "127.0.0.1"

class myHandlerTCP(BaseRequestHandler):
    def handle(self):
        print "TCP connection from ", str(self.client_address)
        while True:
            self.request.send(menuBank())
            accountNumber = self.request.recv(1024) #This is the bank account number
            self.request.send('Introduce your account password:  ')
            accountPassword = self.request.recv(1024)

            if accounts[accountNumber]['password'] == accountPassword:
                accounts[accountNumber]['dyn'] = randint(0, 10)
                self.request.send(menuBank2(str(accounts[accountNumber]['name']),str(accounts[accountNumber]['dyn'])))
                data = self.request.recv(1024)

                if data == '0':                                         #Check the balance
                    self.request.send('inf')
                    sleep(0.5)
                    self.request.send('Your balance is: '+str(accounts[accountNumber]['balance']))
                    sleep(2)
                    self.request.send("bye")
                    break

                elif data == '1':                                       #Deposite money
                    self.request.send('Current balance: '+str(accounts[accountNumber]['balance'])+'\nHow much money do you want to deposite?')
                    data = self.request.recv(1024)
                    accounts[accountNumber]['balance'] += int(data)
                    self.request.send('inf')
                    sleep(0.5)
                    self.request.send('Your new balance is: '+str(accounts[accountNumber]['balance']))
                    sleep(2)
                    self.request.send("bye")
                    break

                elif data == '2':                                       #Extract money
                    self.request.send('Current balance: '+str(accounts[accountNumber]['balance'])+'\nHow much money do you want to extract?')
                    data = self.request.recv(1024)
                    accounts[accountNumber]['balance'] -= int(data)
                    self.request.send('inf')
                    sleep(0.5)
                    self.request.send('Your new balance is: '+str(accounts[accountNumber]['balance']))
                    sleep(2)
                    self.request.send("bye")
                    break
                else:
                    self.request.send('bye')
                    break
            else:
                self.request.send('err')
                sleep(0.5)
                self.request.send('Incorrect password')
                sleep(2)
                self.request.send("bye")
                break

        self.request.close()

class myHandlerUDP(BaseRequestHandler):
    def handle(self):
        print "UDP connection from ", str(self.client_address)
        data, conn = self.request
        data = data.split(' ')
        for i in range(len(data)):
            data[i] = decif(data[i])

        if (accounts[data[0]]['password'] == data[1] and accounts[data[0]]['dyn'] == int(data[3])):
            if accounts[data[0]]['balance'] >= int(data[2]):
                accounts[data[0]]['balance'] -= int(data[2])
                conn.sendto('SUCCESS',self.client_address)
            else:
                conn.sendto('FAIL',self.client_address)
        else:
            conn.sendto('ERR',self.client_address)
myTCPServer = ThreadingTCPServer((bankIp,1234),myHandlerTCP)
myUDPServer = ThreadingUDPServer((bankIp,6789),myHandlerUDP)

t1 = Thread(target=myTCPServer.serve_forever)
t = Thread(target=myUDPServer.serve_forever)

t1.start()
t.start()

t1.join()
t.join()
