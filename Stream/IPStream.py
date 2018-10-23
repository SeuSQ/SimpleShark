from Stream.Stream import Stream


class IPStream(Stream):
    """

    IP流对象
    代表一个IP流，包含这个流中的所有数据包以及流的基本信息
    side_a: A端IP地址（流的第一条报文的src）
    side_b: B端IP地址（流的第一条报文的dst）
    packets：流的报文列表
    direct: 流的方向
           -  None 没有方向（初级流对象，可以继续follow）
           -  'A->B' side_a到side_b方向，不可继续follow
           -  'A<-B' side_b到side_a方向，不可继续follow
           -  'A<->B' 双向，不可继续follow

    返回：
        对象本身无返回，调用follow函数将返回被跟踪方向的子流对象

    """
    def __init__(self, stream_id, side_a, side_b, plist, direct=None):
        Stream.__init__(self, stream_id, side_a, side_b, plist, direct)
        if not direct:
            self.packets.sort()

        self.start_time = self.packets[0].time
        self.end_time = self.packets[-1].time

        self.num = len(self.packets)
        self.size = 0
        for p in self.packets:
            self.size += int(p.length)

        self.__buffer = {}

    def __repr__(self):
        if self.direct is None:
            res = '<IPStream #%d>' % self.stream_id
        else:
            res = '<IPStream #%d(%s)>' % (self.stream_id, self.direct)
        return res

    def follow(self, direct):
        """

        follow流跟踪函数
        类似wireshark的流跟踪，具有三个方向
        参数：
            direct： (String) 流的方向，以下三个可选
                    - 'A->B'
                    - 'A<-B'
                    - 'A<->B'
        返回：
            所跟踪方向的IPStream对象，结构与本对象相同，但是不可继续follow

        """
        if self.direct:
            return None
        if direct.upper() == 'A->B':
            if 'A->B' in self.__buffer:
                return self.__buffer['A->B']
            follow_list = []
            for p in self.packets:
                if p.ip.src == self.side_a and p.ip.dst == self.side_b:
                    follow_list.append(p)
            self.__buffer['A->B'] = IPStream(self.stream_id, self.side_a, self.side_b, follow_list, 'A->B')
            return self.__buffer['A->B']

        elif direct.upper() == 'A<-B':
            if 'B->A' in self.__buffer:
                return self.__buffer['B->A']
            follow_list = []
            for p in self.packets:
                if p.ip.src == self.side_b and p.ip.dst == self.side_a:
                    follow_list.append(p)
            self.__buffer['B->A'] = IPStream(self.stream_id, self.side_b, self.side_a, follow_list, 'B->A')
            return self.__buffer['B->A']
        elif direct.upper() == 'A<->B':
            if 'A<->B' in self.__buffer:
                return self.__buffer['A<->B']
            self.__buffer['A<->B'] = IPStream(self.stream_id, self.side_a, self.side_b, self.packets, 'A<->B')
            return self.__buffer['A<->B']
        else:
            return None



