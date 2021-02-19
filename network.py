import socket
import time
import threading
from functions import BinaryFunction

class Network():
    
    def __init__(self, ip, port, subnet_mask):
        
        self.work = True

        self.ip = ip
        self.port = port
        self.subnet_mask = subnet_mask

        self.math = BinaryFunction.NetworkOperations()

        self.lenMessage = 1024
        
        self.network()

    def network(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind((self.ip, self.port))

    def listen(self, core_function):
        while self.work:
            message, addr = self.sock.recvfrom(self.lenMessage)
            core_function(message, addr)
    
    def sendMessage(self, ip, port, message):
        if type(message) is bytes:
            self.sock.sendto(message, (ip, port))
        else:
            self.sock.sendto(message.encode(), (ip, port))

    def sendBroadcastMessage(self, message, p, n, thread = True):
        if thread:
            thr = threading.Thread(target=self.sendBroadcastMessage, name='BroadcastNetwork', args=(message, p, n, False))
            thr.start()
        else:
            if n == None:
                self.work_broadcast = True
                while self.work_broadcast:
                    self.sendMessage(self.get_broadcast_address(), self.port, message)
                    time.sleep(p)
            else:
                while n >= 0:
                    self.sendMessage(self.get_broadcast_address(), self.port, message)
                    n = n - 1
                    time.sleep(p)
    
    def get_network_address(self):
        binary_network_address = self.math.MultiplyAddress(
            address_1=self.ip, 
            address_2=self.subnet_mask)
        return self.math.get_decimal_address(binary_network_address)

    def get_broadcast_address(self):
        binary_broadcast_addr = self.math.SummaryAddress(
            address_1=self.get_network_address(), 
            address_2=self.math.InvertAddress(address=self.subnet_mask))
        return self.math.get_decimal_address(binary_broadcast_addr)