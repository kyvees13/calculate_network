import socket
import threading
import time

class BinaryFunction():

    class Utility():

        def get_binary_address(self, list_):
            list_ = list_.split('.')
            list_ = [int(list_[num]) for num in range(4)]
            return [bin(list_[num]) for num in range(4)]

        def get_full_octet(self, binary):
            binary = binary.replace('0b', '')
            while len(binary) < 8:
                binary = '0' + binary
            return binary

        def get_decimal_address(self, binary_address):
            decimal_list = [str(int(binary_address[num_binary], base=2)) for num_binary in range(4)]
            return '.'.join(decimal_list)

    class Operations(Utility):

        def MulBinary(self, binary_1, binary_2):
            binary_1 = self.get_full_octet(binary_1)
            binary_2 = self.get_full_octet(binary_2)
            list_ = [str(int(binary_1[num]) & int(binary_2[num])) for num in range(8)]
            return '0b' + ''.join(list_)

        def SumBinary(self, binary_1, binary_2):
            binary_1 = self.get_full_octet(binary_1)
            binary_2 = self.get_full_octet(binary_2)
            list_ = [str(int(binary_1[num]) | int(binary_2[num])) for num in range(8)]
            return '0b' + ''.join(list_)

        def InvertBinary(self, binary):
            binary = self.get_full_octet(binary)
            list_ = [str(int(not int(binary[num]))) for num in range(8)]
            return '0b' + ''.join(list_)

    class NetworkOperations(Operations):

        def MultiplyAddress(self, address_1, address_2):
            address_1 = self.get_binary_address(address_1)
            address_2 = self.get_binary_address(address_2)
            new_address = [self.MulBinary(address_1[num_octet], address_2[num_octet]) for num_octet in range(4)] 
            return (new_address)

        def SummaryAddress(self, address_1, address_2):
            address_1 = self.get_binary_address(address_1)
            address_2 = self.get_binary_address(address_2)
            new_address = [self.SumBinary(address_1[num_octet], address_2[num_octet]) for num_octet in range(4)] 
            return new_address

        def InvertAddress(self, address):
            address = self.get_binary_address(address)
            new_address = [self.InvertBinary(address[num_binary]) for num_binary in range(4)]
            return self.get_decimal_address(new_address)

class Network():
    
    def __init__(self, ip, port, subnet_mask):
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


if __name__ == "__main__":

    ip = '192.168.1.255'
    mask = '255.255.222.0'

    port = '8080'

    Network = Network(ip=ip, port=port, subnet_mask=mask)

    network_addr = Network.get_network_address()
    broadcast_addr = Network.get_broadcast_address()

    print('Network Address: {}\nSubnet Mask:{}\nIPv4: {}\nBroadcast Address: {}'.format(network_addr, mask, ip, broadcast_addr))
    


              

