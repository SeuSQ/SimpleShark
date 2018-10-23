class ISAKMP:
    """
    ISAKMP层对象
    protocol是本层协议名称
    """
    def __init__(self, ispi, rspi, mid, extype, length, close, protocol):
        self.ispi = ispi
        self.rspi = rspi
        self.mid = mid
        self.extype = extype
        self.length = length
        self.close = close
        self.protocol = protocol

    def __repr__(self):
        return '<%s Layer>' % self.protocol.upper()
