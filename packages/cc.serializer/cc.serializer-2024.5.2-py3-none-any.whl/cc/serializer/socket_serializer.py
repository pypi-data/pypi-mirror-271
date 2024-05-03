
from .serializer import Serializer


class SocketSerializer(Serializer):
    def __init__(self, connection, buffered_transmit=False):
        self._conn = connection
        self.buffered_transmit = buffered_transmit
        self.tx_buffer = b""

    """
    Set a timeout on blocking socket operations. 
    
    The value argument can be a nonnegative floating point number expressing seconds, or None. 
    If a non-zero value is given, subsequent socket operations will raise a timeout exception if the timeout period value has elapsed before the operation has completed. 
    If zero is given, the socket is put in non-blocking mode. 
    If None is given, the socket is put in blocking mode.
    """
    def setReceiveTimeout(self, timeout):
        self._conn.settimeout(timeout)

    def _receive(self, size, timeout=None):
        try:
            data = self._conn.recv(size)
            return data
        except TimeoutError:
            return b""
    
    def _transmit(self, data, size):
        if self.buffered_transmit:
            self.tx_buffer += data
        self._conn.sendall(data)
    
    def _flush(self):
        if self.buffered_transmit:
            self._conn.sendall(self.tx_buffer)
        self.tx_buffer = b""
