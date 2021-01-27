from SocketServer import ForkingTCPServer, BaseRequestHandler, ThreadingTCPServer
from socket import *
from menu import *
from os import system
from time import sleep

system("clear||cls")
print "Liquor Store is open!"
#print ("Recuerde que la conexion es con NC 127.0.0.1 3456")
sockets = []
liquors = [
    {'code':0, 'name':'Aguardiente Antioquenio', 'src': 'CO', 'stock':10, 'price': 41600},
    {'code':1, 'name':'Whisky old parr 12 anios', 'src': 'GB-SCT', 'stock':9, 'price': 105990},
    {'code':2, 'name':'Crema de whisky baileys', 'src': 'IE', 'stock':8, 'price': 76000},
    {'code':3, 'name':'Vino Tinto Chileno Cabernet Fuego Austral Sauvignon', 'src': 'CL', 'stock':7, 'price': 25900},
    {'code':4, 'name':'Ron Viejo de Caldas Gran Reserva Carta De Oro 8 anios', 'src': 'CO', 'stock':5, 'price': 69400}
    ]

class myHandler(BaseRequestHandler):

    def handle(self):
        returnBan = False
        print "Connection from ", str(self.client_address)
        sockets.append(str(self.client_address))
        print sockets
        self.request.send('\n'+menuLiquor()+"\nOnline users: "+str(len(sockets))+"\n")

        while True:
            if returnBan == True:
                self.request.send('\n'+menuLiquor()+"\nOnline users: "+str(len(sockets))+"\n")
                returnBan = False
            data = self.request.recv(1024)
            if data == '1':
                self.request.send('\n')
                for i in liquors:
                    self.request.send('[+] '+i['name']+', origen: '+i['src']+', stock: '+str(i['stock'])+', unit price: '+str(i['price'])+'\n')
                self.request.send('\n'+menuLiquor2())
                data = self.request.recv(1024)
                if data == '1': #return to main menu
                    returnBan = True

            elif data == '2':
                self.request.send('Which drink do you want to buy?\n')
                count = 0
                for i in liquors:
                    self.request.send('['+str(count)+'] '+i['name']+', origen: '+i['src']+', stock: '+str(i['stock'])+', unit price: '+str(i['price'])+'\n')
                    count = count+1
                liquor = int(self.request.recv(1024))

                self.request.send('How many units?')
                units = int(self.request.recv(1024))

                bill = liquors[liquor]['price']*units

                self.request.send('Total price: '+str(bill)+'\n\nSending to the BANK server...\n\nIntroduce your account number: ')
                accountNumber = self.request.recv(1024) #son str que asi es como estan guardados en el bank.py
                
                self.request.send('Introduce your account password: ')
                accountPassword = self.request.recv(1024)

                c = socket(AF_INET,SOCK_DGRAM)
                c.sendto(accountNumber+' '+accountPassword+' '+str(bill),("localhost",6789))
                data2,remote_host = c.recvfrom(1024)
                if data2=='SUCCESS':
                    self.request.send("thx") #exito en la compra
                    sleep(0.9)
                    sockets.remove(str(self.client_address))
                    break
                else:
                    self.request.send("nomo") #error en la compra por falta de dinero
                    sleep(0.9)
                    sockets.remove(str(self.client_address))
                    break
            elif data == '3':
                sockets.remove(str(self.client_address))
                break
            #self.request.send(data.upper())
        #self.request.send("Bye my brother, press Enter ;)\n")
        self.request.send("bye")
        self.request.close()

'''   def broadcast_string(self, b_msg, skip_socket):
        for socket in SOCKETS_LIST:
            if socket != myServer and socket != skip_socket:
                socket.send(b_msg)
        print b_msg'''

myServer = ThreadingTCPServer(("127.0.0.1", 3456), myHandler)
myServer.serve_forever()