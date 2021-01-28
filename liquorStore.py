from SocketServer import BaseRequestHandler, ThreadingTCPServer
from socket import *
from menu import *
from os import system
from time import sleep
from cesar import *

system("clear||cls")
print "Liquor Store is open!"
liquorIp = "127.0.0.1"
bankIp = "127.0.0.1"
sockets = []
liquors = [
    {'code':0, 'name':'Aguardiente Antioquenio', 'src': 'CO', 'stock':10, 'price': 41600},
    {'code':1, 'name':'Whisky old parr 12 anios', 'src': 'GB-SCT', 'stock':9, 'price': 105990},
    {'code':2, 'name':'Crema de whisky baileys', 'src': 'IE', 'stock':8, 'price': 76000},
    {'code':3, 'name':'Vino Tinto Chileno Cabernet Fuego Austral Sauvignon', 'src': 'CL', 'stock':7, 'price': 25900},
    {'code':4, 'name':'Ron Viejo de Caldas Gran Reserva Carta De Oro 8 anios', 'src': 'CO', 'stock':5, 'price': 69400}
    ]

def liquorart():
    art = """    )        (                   (
   (          )     (             )
    )    *           )        )  (
   (                (        (      *
    )          H     )        )
              [ ]            (
       (  *   |-|       *     )    (
 *      )     |_|        .          )
       (      | |    .  
 )           /   \     .    ' .        *
(           |_____|  '  .    .  
 )          | ___ |  \~~~/  ' .   (
        *   | \ / |   \_/  \~~~/   )
            | _Y_ |    |    \_/   (
*           |-----|  __|__   |      *
            `-----`        __|__"""
    return art

class myHandler(BaseRequestHandler):

    def handle(self):
        returnBan = False
        print "Connection from ", str(self.client_address)
        sockets.append(str(self.client_address))
        self.request.send(menuLiquor()+"\nOnline users: "+str(len(sockets)))

        while True:
            if returnBan == True:
                self.request.send(menuLiquor()+"\nOnline users: "+str(len(sockets)))
                returnBan = False
            data = self.request.recv(1024)
            if data == '1':
                self.request.send('Liquor list:\n\n')
                for i in liquors:
                    self.request.send('[+] '+i['name']+', source: '+i['src']+', stock: '+str(i['stock'])+', unit price: '+str(i['price'])+'\n')
                self.request.send('\n'+menuLiquor2()+"\nOnline users: "+str(len(sockets)))
                data = self.request.recv(1024)
                if data == '1': #return to main menu
                    returnBan = True

            elif data == '2':
                self.request.send('Which drink do you want to buy?\n\n')
                count = 0
                for i in liquors:
                    self.request.send('['+str(count)+'] '+i['name']+', source: '+i['src']+', stock: '+str(i['stock'])+', unit price: '+str(i['price'])+'\n')
                    count = count+1
                self.request.send("\nOnline users: "+str(len(sockets)))

                liquor = int(self.request.recv(1024))

                self.request.send('How many units?\nRemember that we only have '+str(liquors[liquor]['stock'])+' units of '+liquors[liquor]['name'])
                units = int(self.request.recv(1024))

                bill = liquors[liquor]['price']*units

                self.request.send('Total price: '+str(bill)+'\n\nSending to the BANK server...\n\nIntroduce your account number: ')
                accountNumber = self.request.recv(1024) #son str que asi es como estan guardados en el bank.py
                accountNumber = cif(accountNumber)
                
                self.request.send('Introduce your account password: ')
                accountPassword = self.request.recv(1024)
                accountPassword = cif(accountPassword)

                self.request.send('Introduce your dynamic key: ')
                accountKey = self.request.recv(1024)
                accountKey = cif(accountKey)

                bill = cif(str(bill))

                c = socket(AF_INET,SOCK_DGRAM)
                c.sendto(accountNumber+' '+accountPassword+' '+bill+' '+accountKey,(bankIp,6789))
                data2,remote_host = c.recvfrom(1024)

                if data2=='SUCCESS':
                    liquors[liquor]['stock'] -= units
                    self.request.send("thx") #exito en la compra
                    sleep(0.9)
                    self.request.send("Thanks for your buy!\nEnjoy your drink\n"+liquorart())
                    sleep(1.5)
                    sockets.remove(str(self.client_address))
                    break
                elif data2 == 'FAIL':
                    self.request.send("inf") #error en la compra por falta de dinero
                    sleep(0.9)
                    self.request.send("You do not have enough money")
                    sleep(0.9)
                    sockets.remove(str(self.client_address))
                    break
                else:
                    self.request.send("inf") #error en la compra por falta de dinero
                    sleep(0.9)
                    self.request.send("Incorrect password or key")
                    sleep(0.9)
                    sockets.remove(str(self.client_address))
                    break
            elif data == '3':
                sockets.remove(str(self.client_address))
                break
        self.request.send("bye")
        self.request.close()

myServer = ThreadingTCPServer((liquorIp, 3456), myHandler)
myServer.serve_forever()
