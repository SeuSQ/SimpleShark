from Stream.ESPStream import ESPStream
from Stream.IPStream import IPStream
from Stream.TransportStream import TransportStream


class StreamExtractor:
    """

    流提取器类
    从数据报列表中提取IP/TCP/UDP等层级的流，类似wireshark中的对话
    参数：
        plist：（List）一个Packet数据报列表
    返回：
        对象本身无返回值，需要调用具体的解析函数

    """
    def __init__(self, plist):
        self.packets = plist

    def extractor(self):
        self.ex_ip_stream()

    def ex_ip_stream(self):
        """

        解析IP流
        返回：
            一个IPStream列表

        """
        ip_stream_list = []
        ip_stream_dict = {}
        for p in self.packets:
            # 用IPa|IPb与IPb|IPa唯一标记一个流，这两者等价
            ip_pair1 = '%s|%s' % (p.ip.src, p.ip.dst)
            ip_pair2 = '%s|%s' % (p.ip.dst, p.ip.src)
            # 如果两种标记都没出现过，说明流是第一次出现
            if ip_pair1 not in ip_stream_dict and ip_pair2 not in ip_stream_dict:
                ip_stream_dict[ip_pair1] = []
                ip_stream_dict[ip_pair1].append(p)
                continue

            # 数据报第一次以上出现
            if ip_pair1 in ip_stream_dict:
                ip_stream_dict[ip_pair1].append(p)
                continue
            if ip_pair2 in ip_stream_dict:
                ip_stream_dict[ip_pair2].append(p)
                continue

        # 遍历临时列表，生成IPStream对象
        i = 0
        for key in ip_stream_dict:
            side_a, side_b = key.split('|')
            ip_stream_list.append(IPStream(i, side_a, side_b, ip_stream_dict[key]))
            i += 1

        return ip_stream_list

    def ex_esp_stream(self):
        """

        解析ESP流
        返回：
            一个 ESPStream列表
        """
        esp_stream_list = []
        esp_stream_dict = {}
        esp_spi = set()
        for p in self.packets:
            if 'ESP' not in p:
                continue

            esp_pair1 = '%s|%s' % (p.ip.src, p.ip.dst)
            esp_pair2 = '%s|%s' % (p.ip.dst, p.ip.src)
            # 如果两种标记都没出现过，说明流是第一次出现
            if esp_pair1 not in esp_stream_dict and esp_pair2 not in esp_stream_dict:
                esp_stream_dict[esp_pair1] = []
                esp_stream_dict[esp_pair1].append(p)
                esp_spi.add(p.esp.spi)
                continue

            # 数据报第一次以上出现
            if esp_pair1 in esp_stream_dict:
                esp_stream_dict[esp_pair1].append(p)
                esp_spi.add(p.esp.spi)
                continue
            if esp_pair2 in esp_stream_dict:
                esp_stream_dict[esp_pair2].append(p)
                esp_spi.add(p.esp.spi)
                continue

        # 发现两个以上SPI，说明有不止一个ESP连接，无法分辨
        if len(esp_spi) > 2:
            raise UserWarning('more than one esp pair')

        # 遍历临时列表，生成IPStream对象
        i = 0
        for key in esp_stream_dict:
            side_a, side_b = key.split('|')
            esp_stream_list.append(ESPStream(i, side_a, side_b, esp_stream_dict[key], list(esp_spi)))
            i += 1

        return esp_stream_list

    def ex_udp_stream(self):
        """

        解析UDP流
        返回:
            一个具有UDP类型标记的TransportStream列表

        """
        udp_stream_list = []
        udp_stream_dict = {}
        for p in self.packets:
            if 'UDP' not in p:
                continue

            stream_id = p.udp.stream
            if stream_id not in udp_stream_dict:
                udp_stream_dict[stream_id] = []
                udp_stream_dict[stream_id].append(p)
                continue

            if stream_id in udp_stream_dict:
                udp_stream_dict[stream_id].append(p)
                continue

        for key in udp_stream_dict:
            plist = udp_stream_dict[key]
            udp_stream_list.append(TransportStream(plist[0].udp.protocol,
                                                   plist[0].ip.src,
                                                   plist[0].ip.dst,
                                                   plist[0].udp.src,
                                                   plist[0].udp.dst,
                                                   plist,
                                                   plist[0].udp.stream))

        return udp_stream_list

    def ex_tcp_stream(self):
        """

        解析TCP流
        返回:
            一个具有TCP类型标记的TransportStream列表

        """
        tcp_stream_list = []
        tcp_stream_dict = {}
        for p in self.packets:
            if 'TCP' not in p:
                continue

            stream_id = p.tcp.stream
            if stream_id not in tcp_stream_dict:
                tcp_stream_dict[stream_id] = []
                tcp_stream_dict[stream_id].append(p)
                continue

            if stream_id in tcp_stream_dict:
                tcp_stream_dict[stream_id].append(p)
                continue

        for key in tcp_stream_dict:
            plist = tcp_stream_dict[key]
            tcp_stream_list.append(TransportStream(plist[0].tcp.protocol,
                                                   plist[0].ip.src,
                                                   plist[0].ip.dst,
                                                   plist[0].tcp.src,
                                                   plist[0].tcp.dst,
                                                   plist,
                                                   plist[0].tcp.stream))

        return tcp_stream_list
