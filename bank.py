from SocketServer import ThreadingUDPServer, ThreadingTCPServer, BaseRequestHandler
from threading import Thread
from menu import *
from os import system
from time import sleep

system("clear||cls")
print "Bank is open!"
accounts = {'000':{'name': 'Mateo Jaramillo', 'password':'mateo123', 'balance':318890},
    '001':{'name': 'Daniela Jurado', 'password':'daniela123', 'balance':3200000},
    '002':{'name': 'Luis Carlos', 'password':'carlos123', 'balance':3000}
    #'002':{'name': 'Luis Carlos', 'password':'carlos789', 'balance':300000}
}

class myHandlerTCP(BaseRequestHandler):
    def handle(self):
        print "TCP Connection from ", str(self.client_address)
        while True:
            self.request.send(menuBank())
            accountNumber = self.request.recv(1024) #This is the bank account number
            self.request.send('Introduce your account password:  ')
            accountPassword = self.request.recv(1024)

            if accounts[accountNumber]['password'] == accountPassword:
                self.request.send(menuBank2(str(accounts[accountNumber]['name'])))
                data = self.request.recv(1024)

                if data == '0':                                         #Check the balance
                    self.request.send('inf')
                    sleep(0.5)
                    self.request.send('Your balance is: '+str(accounts[accountNumber]['balance']))
                    sleep(2)
                    self.request.send("bye")
                    break

                elif data == '1':                                       #Deposite money
                    self.request.send('How much money do you want to deposite?')
                    data = self.request.recv(1024)
                    accounts[accountNumber]['balance'] += int(data)
                    self.request.send('inf')
                    sleep(0.5)
                    self.request.send('Your new balance is: '+str(accounts[accountNumber]['balance']))
                    sleep(2)
                    self.request.send("bye")
                    break

                elif data == '2':                                       #Extract money
                    self.request.send('How much money do you want to extract?')
                    data = self.request.recv(1024)
                    accounts[accountNumber]['balance'] -= int(data)
                    self.request.send('inf')
                    sleep(0.5)
                    self.request.send('Your new balance is: '+str(accounts[accountNumber]['balance']))
                    sleep(2)
                    self.request.send("bye")
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
        print "UDP Connection from ", str(self.client_address)
        data, conn = self.request
        data = data.split(' ')

        if accounts[data[0]]['balance'] >= int(data[2]):
            accounts[data[0]]['balance'] -= int(data[2])
            conn.sendto('SUCCESS',self.client_address)
        else:
            conn.sendto('FAIL',self.client_address)

myTCPServer = ThreadingTCPServer(('127.0.0.1',1234),myHandlerTCP)
myUDPServer = ThreadingUDPServer(('127.0.0.1',6789),myHandlerUDP)

print 'ChatServerTCP started on port %s' % 1234
print 'ChatServerUDP started on port %s' % 6789

t1 = Thread(target=myTCPServer.serve_forever)
t = Thread(target=myUDPServer.serve_forever)

t1.start()
t.start()

t1.join()
t.join()