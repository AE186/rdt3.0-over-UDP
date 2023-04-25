import socket
import select
import json
from base_rdt import base_rdt

class sender(base_rdt):
    def __init__(self, ip, port, timeout, MSS) -> None:
        super().__init__()
        self.senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.senderSocket.settimeout(timeout)

        self.addr = (ip, port)
        self.timeout = timeout
        self.MSS = MSS - len(self.make_pkt(''))

    def snd_pkt(self, sndpkt):
        while True:
            self.senderSocket.sendto(sndpkt.encode(), self.addr)
            rcv_pkt = None

            read, write, err = select.select([self.senderSocket], [], [], self.timeout)
            for s in read:
                rcv_pkt, _ = s.recvfrom(self.MSS)
                rcv_pkt = rcv_pkt.decode()
                rcv_pkt = json.loads(rcv_pkt)            
            if rcv_pkt is not None and not self.corrupt(rcv_pkt) and self.has_seq(rcv_pkt):
                break
            elif rcv_pkt is not None and len(rcv_pkt) == 0:
                break

    def send(self, msg):
        i=0
        while i <= len(msg):
            snd_pkt = self.make_pkt(msg[i:i+self.MSS])
            self.snd_pkt(snd_pkt)
            self.seq = 0 if self.seq == 1 else 1
            i += self.MSS
        
        snd_pkt = self.make_pkt('\r\nEND\r\n')
        self.snd_pkt(snd_pkt)
        

sock = sender('localhost', 9999, 0.7, 150)
with open('msg.txt') as f:
    sock.send(f.read())
