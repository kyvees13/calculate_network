from network import Network
from functions import BinaryFunction
import threading

class Application():
    
    def __init__(self):

        self.ip = '192.168.1.101'
        self.port = 8080

        self.subnet_mask = '255.255.255.0'

        self.net = Network(ip=self.ip, port=self.port, subnet_mask=self.subnet_mask)
        self.network_addr = self.net.get_network_address()
        self.broadcast_addr = self.net.get_broadcast_address()
        print('Network Address: {}\nSubnet Mask:{}\nIP address: {}\nBroadcast Address: {}'.format(self.network_addr, self.subnet_mask, self.ip, self.broadcast_addr))

        self.listenThread = threading.Thread(target=self.net.listen, name='listenNetwork', args=(self.core,))
        self.listenThread.start()

        self.my_name = '\n'
        self.sendHello()

    def sendHello(self):
        message = self.my_name
        self.net.sendBroadcastMessage(message, 1, 5, None)

    def core(self, data, addr):
        if data is not bytes:
            data = data.decode('utf-8')
        print('\nПолучено сообщение', data, addr)

if __name__ == '__main__':

    app = Application()


