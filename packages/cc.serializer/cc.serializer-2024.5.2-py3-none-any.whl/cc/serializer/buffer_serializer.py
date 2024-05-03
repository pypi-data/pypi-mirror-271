
from .serializer import Serializer

class BufferSerializer(Serializer):
    def __init__(self):
        self.tx_buffer = b""
        self.rx_buffer = b""

    def _receive(self, size):
        r = self.rx_buffer[:size]
        self.rx_buffer = self.rx_buffer[size:]
        return r
    
    def _transmit(self, data, size):
        self.tx_buffer += data

    def encode(self, data):
        self.tx_buffer = b""
        self.transmit(data)
        return self.tx_buffer
    
    def decode(self, data):
        self.rx_buffer = data
        return self.receive()

