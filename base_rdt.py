import json

class base_rdt:
    def __init__(self):
        self.seq = 0
    
    def cal_checksum(self, data):
        sum = 0
        i=0
        data = data.encode()
        while i < len(data):
            sum += int.from_bytes(data[i:i+2], 'big')
            if sum >= 2**17-1:
                sum = format(sum, '17b')[1:]
                sum = int(sum, 2) + 1
            i = i+2
        
        complement = ''.join('0' if i=='1' else '1' for i in format(sum, '16b'))

        return int(complement, 2)

    def make_pkt(self, msg, isACK=False):
        data = {
            'seq': self.seq,
            'ack': 1 if isACK else 0,
            'msg': msg
        }
        data = json.dumps(data)

        pkt = {
            'data': data,
            'checksum': self.cal_checksum(data)
        }
        pkt = json.dumps(pkt)

        return pkt
    
    def make_ACK(self):
        return self.make_pkt('', True)

    def corrupt(self, pkt):
        data = pkt['data']
        checksum = pkt['checksum']

        if checksum == self.cal_checksum(data):
            return False
        
        return True

    def has_seq(self, pkt):
        data = self.get_data(pkt)
        
        if data['seq'] == self.seq:
            return True
        
        return False
    
    def get_data(self, pkt):
        return json.loads(pkt["data"])