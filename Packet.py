class Packet:
    """

    数据报实体类
    一个packet对象代表一条数据报
    参数：
        number：（int）数据报在wireshark中的编号
        length： （int）数据报总长度（字节）
        sniff_time： （Time）报文捕获时间
        transport_layer： （String） 传输层协议类型

    """
    def __init__(self, number, length, sniff_time, transport_layer):
        self.layers = []
        self.number = number
        self.length = length
        self.time = sniff_time
        self.transport_layer = transport_layer

    def get_top_protocol(self):
        """

        获得顶层协议的对象

        """
        return self.layers[-1]

    def add_layer(self, layer):
        """

        添加一个协议层
        只在文件解析阶段被调用

        """
        self.layers.append(layer)

    def __getattr__(self, item):
        """

        属性访问魔法方法
        直接使用点语法获取各层级对象。例如：
        packet.eth
        packet.ip
        packet.tcp
        packet.top_ptl (最高层协议名称)

        """
        for layer in self.layers:
            if layer.protocol == item.lower():
                return layer

        if item == 'top_ptl':
            return self.layers[-1].protocol.upper()

        raise AttributeError("No attribute named %s" % item)

    def __repr__(self):
        transport_protocol = ''
        if self.transport_layer != self.top_ptl and self.transport_layer is not None:
            transport_protocol = self.transport_layer + '/'

        return '<%s%s Packet>' % (transport_protocol, self.top_ptl)

    def __lt__(self, other):
        """

        重载 < 操作符
        进行比较操作时，packet对象将以时间为主键进行升序排列

        """
        if self.time < other.time:
            return True
        return False

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.layers[item]
        for layer in self.layers:
            if layer.protocol == item.lower():
                return layer
        raise KeyError('Layer does not exist in packet')

    def __contains__(self, item):
        """

        属性包含魔法方法
        可直接使用如下语句判断数据报内是否包含某一层协议
        if 'IP' in packet:
            do something
        """
        try:
            self[item]
            return True
        except KeyError:
            return False
