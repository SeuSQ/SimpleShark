class Ethernet:
    """
    以太层对象
    protocol是本层协议名称
    """
    def __init__(self, src, dst, protocol):
        self.src = src
        self.dst = dst
        self.protocol = protocol

    def __repr__(self):
        return '<%s Layer>' % self.protocol.upper()