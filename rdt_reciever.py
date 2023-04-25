import socket
import json
from base_rdt import base_rdt

class receiver(base_rdt):
    def __init__(self, ip, port, buff) -> None:
        super().__init__()
        self.receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiverSocket.bind((ip, port))
        self.buff = 1024
    
    def recv(self):
        rbuff = ''
        while True:
            rcv_pkt, addr = self.receiverSocket.recvfrom(self.buff)
            rcv_pkt = rcv_pkt.decode()
            rcv_pkt = json.loads(rcv_pkt)

            if not self.corrupt(rcv_pkt) and self.has_seq(rcv_pkt):
                data = self.get_data(rcv_pkt)
                self.seq = 0 if self.seq == 1 else 1

                snd_pkt = self.make_ACK()
                self.receiverSocket.sendto(snd_pkt.encode(), addr)

                if data['msg'] == '\r\nEND\r\n':
                    break

                rbuff += data['msg']
        
        return rbuff


sock = receiver('localhost', 9999, 1024)
msg = sock.recv()
print(msg)
