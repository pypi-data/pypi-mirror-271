import struct


class Encoding:
    END         = b"\x0A"
    ESC         = b"\x0B"
    ESC_END     = b"\x1A"
    ESC_ESC     = b"\x1B"

class Serializer:
    def __init__(self):
        pass

    def _receive(self, size):
        pass

    def _transmit(self, data, size):
        pass

    def _flush(self):
        pass

    def setReceiveTimeout(self, timeout):
        pass

    def setTransmitTimeout(self, timeout):
        pass

    """
    Receive a packet from serial.

    @type timeout: float
    @param timeout: 
    @return: the data received, or b"" if no data is available
    """
    def receive(self, timeout=None):
        data = b""
        c = self._receive(1)

        while c != Encoding.END:
            if c == Encoding.ESC:
                c = self._receive(1)
                if c == Encoding.ESC_END:
                    data += Encoding.END
                elif c == Encoding.ESC_ESC:
                    data += Encoding.ESC
                else:
                    data += c
            else:
                data += c
            c = self._receive(1)
        return data

    """
    Transmit a packet to serial.

    @type data: bytes
    @param data: the data that will be sent.
    """
    def transmit(self, data):
        if type(data) == str:
            raise AttributeError("cannot transmit \"str\" object. Perhaps try \"str.encode()\" it?")

        index = 0
        while index < len(data):
            c = struct.pack("B", data[index])
            if c == Encoding.END:
                self._transmit(Encoding.ESC, 1)
                self._transmit(Encoding.ESC_END, 1)
            elif c == Encoding.ESC:
                self._transmit(Encoding.ESC, 1)
                self._transmit(Encoding.ESC_ESC, 1)
            else:
                self._transmit(c, 1)
            index += 1
        self._transmit(Encoding.END, 1)

        self._flush()
