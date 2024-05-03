import serial
import serial.tools.list_ports

from .serializer import Encoding, Serializer


class UARTSerializer(Serializer):
    def __init__(self, port=None, baudrate=115200):
        self._port = port
        self.baudrate = baudrate

        if not self._port:
            # if no port is supplied, we enumerate the available ports
            # and try the first one
            ports = UARTSerializer.getAvailablePorts()
            if ports:
                self._port = ports[0]
                print("No \"port\" argument supplied, using {0}.".format(self._port))

        self._ser = serial.Serial(
            port=self._port, baudrate=baudrate, timeout=None)

    @staticmethod
    def getAvailablePorts():
        ports = [p.name for p in serial.tools.list_ports.comports()]
        return ports
        
    """
    timeout = None: wait forever / until requested number of bytes are received
    timeout = 0: non-blocking mode, return immediately in any case, returning zero or more, up to the requested number of bytes
    timeout = x: set timeout to x seconds (float allowed) returns immediately when the requested number of bytes are available, otherwise wait until the timeout expires and return all bytes that were received until then.
    """
    def setReceiveTimeout(self, timeout):
        self._ser.timeout = timeout
        
    def setTransmitTimeout(self, timeout):
        self._ser.write_timeout = timeout

    def _receive(self, size):
        return self._ser.read(size)
    
    def _transmit(self, data, size):
        self._ser.write(data)
