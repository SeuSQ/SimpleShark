class TCP:
    """
    TCP层对象
    protocol是本层协议名称
    """
    def __init__(self, src, dst, stream, length, seq, ack, time_delta, time_relative, protocol):
        self.src = src
        self.dst = dst
        self.length = length
        self.stream = stream
        self.seq = seq
        self.ack = ack
        self.time_delta = time_delta
        self.time_relative = time_relative
        self.protocol = protocol

    def __repr__(self):
        return '<%s Layer>' % self.protocol.upper()