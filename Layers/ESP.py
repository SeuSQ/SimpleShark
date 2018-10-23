class ESP:
    """
    ESP层对象
    protocol是本层协议名称
    """
    def __init__(self, spi, seq, protocol, over_udp):
        self.spi = spi
        self.seq = seq
        self.protocol = protocol
        self.over_udp = over_udp

    def __repr__(self):
        if self.over_udp:
            return '<%s Layer over UDP>' % self.protocol.upper()
        else:
            return '<%s Layer>' % self.protocol.upper()
