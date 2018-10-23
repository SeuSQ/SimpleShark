from Stream.Stream import Stream


class ESPStream(Stream):
    def __init__(self, stream_id, side_a, side_b, plist, spi, direct=None):
        Stream.__init__(self, stream_id, side_a, side_b, plist, direct)
        self.spi = spi

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
            res = '<ESPStream #%d>' % self.stream_id
        else:
            res = '<ESPStream #%d(%s)>' % (self.stream_id, self.direct)
        return res

    def follow(self, direct):
        if self.direct:
            return None
        if direct.upper() == 'A->B':
            if 'A->B' in self.__buffer:
                return self.__buffer['A->B']
            follow_list = []
            for p in self.packets:
                if p.ip.src == self.side_a and p.ip.dst == self.side_b:
                    follow_list.append(p)
            self.__buffer['A->B'] = ESPStream(self.stream_id, self.side_a, self.side_b, follow_list, follow_list[0].esp.spi ,'A->B')
            return self.__buffer['A->B']
        elif direct.upper() == 'A<-B':
            if 'A<-B' in self.__buffer:
                return self.__buffer['A<-B']
            follow_list = []
            for p in self.packets:
                if p.ip.src == self.side_a and p.ip.dst == self.side_b:
                    follow_list.append(p)
            self.__buffer['A<-B'] = ESPStream(self.stream_id, self.side_b, self.side_a, follow_list, follow_list[0].esp.spi ,'A<-B')
            return self.__buffer['A<-B']
        elif direct.upper() == 'A<->B':
            if 'A<->B' in self.__buffer:
                return self.__buffer['A<->B']
            self.__buffer['A<->B'] = ESPStream(self.stream_id, self.side_a, self.side_b, self.packets, self.spi, 'A<->B')
            return self.__buffer['A<->B']
        else:
            return None
