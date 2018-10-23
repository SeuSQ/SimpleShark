class IPv4:
    """
    IPv4层对象
    protocol是本层协议名称
    """
    def __init__(self, src, dst, length, protocol):
        self.src = src
        self.dst = dst
        self.length = length
        self.protocol = protocol

    def __repr__(self):
        return '<%s Layer>' % self.protocol.upper()
