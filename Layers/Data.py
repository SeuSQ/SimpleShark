class Data:
    """
    DATA层对象
    protocol是本层协议名称

    在检测到未知协议或不关注具体协议的情况下，可默认使用DATA层
    """
    def __init__(self):
        self.protocol = 'DATA'

    def __repr__(self):
        return '<%s Layer>' % self.protocol.upper()
