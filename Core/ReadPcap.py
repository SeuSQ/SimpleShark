import sys
import time

import pyshark

from Layers.Data import Data
from Layers.ESP import ESP
from Layers.Ethernet import Ethernet
from Layers.IPv4 import IPv4
from Layers.ISAKMP import ISAKMP
from Layers.TCP import TCP
from Layers.UDP import UDP
from Core.Packet import Packet


def ReadPcap(path, dis_filter=None):

    """

    pcap解析类
    将pcap及pcapng文件解析为本代码的数据结构，只保留各层的头部信息，数据部分将被舍弃

    参数：cap = pyshark.FileCapture(path, display_filter=dis_filter, keep_packets=False)
        path：(String) 需要被解析的文件的路径
        dis_filter: (String) 数据报过滤器，可直接使用wireshark的显示过滤器语法

    返回：
        经过解析的packet列表（List）

    """

    packets = []
    try:
        cap = pyshark.FileCapture(path, display_filter=dis_filter, keep_packets=False)
    except Exception:
        print('Read file error!')
        return None

    i = 1
    start_time = time.time()
    for p in cap:
        # 判断是否包含传输层协议，如果没有这个数据包会被直接舍弃
        sys.stdout.write('\rNow at packet #%d' % i)
        sys.stdout.flush()
        i += 1
        if p.transport_layer is not None:
            pobj = Packet(p.number, p.length, p.sniff_time, p.transport_layer)
        else:
            # 非NAT环境下的ESP包没有传输层，需要在这里处理一下
            if 'ESP' in p:
                pobj = Packet(p.number, p.length, p.sniff_time, 'ESP')
            else:
                continue

        # 链路层
        if 'ETH' in p:
            pobj.add_layer(Ethernet(p.eth.src, p.eth.dst, p.eth.layer_name))

        # 网络层 只解析IPv4数据报
        if 'IP' in p:
            pobj.add_layer(IPv4(p.ip.src, p.ip.dst, p.ip.len, p.ip.layer_name))
        else:
            continue

        # 传输层
        if 'UDP' in p:
            pobj.add_layer(UDP(p.udp.srcport, p.udp.dstport, p.udp.stream, p.udp.length, p.udp.layer_name))
        elif 'TCP' in p:
            pobj.add_layer(TCP(p.tcp.srcport, p.tcp.dstport, p.tcp.stream, p.tcp.len, p.tcp.seq, p.tcp.ack,
                               p.tcp.time_delta, p.tcp.time_relative, p.tcp.layer_name))

        # IKE & ESP
        if 'ISAKMP' in p:
            if p.isakmp.nextpayload == '46' and p.isakmp.nextpayload.fields[1].raw_value == '2a':
                isclose = True
            else:
                isclose = False
            pobj.add_layer(ISAKMP(p.isakmp.ispi, p.isakmp.rspi, p.isakmp.messageid, p.isakmp.exchangetype,
                                  p.isakmp.length, isclose, 'ISAKMP'))
        elif 'ESP' in p:
            # 处理UDP封装的ESP
            if 'UDP' in p:
                pobj.add_layer(ESP(p.esp.spi, p.esp.sequence, 'esp', True))
            else:
                pobj.add_layer(ESP(p.esp.spi, p.esp.sequence, 'esp', False))
        else:
            """
            请在此处扩展可解析的顶层协议（需要先编写对应协议的对象文件并引入）
            """
            pobj.add_layer(Data())
            # TSL\SSL\GQUIC\HTTP(S)

        packets.append(pobj)
    end_time = time.time()
    use_time = end_time - start_time
    speed = i / use_time
    print('\nParse packets completed, speed: %dpps' % int(speed))
    print('======================================\n')
    return packets


if __name__ == '__main__':
    res = ReadPcap("C:\\Users\\Hikari\\Desktop\\ipse实验\\连接建立阶段.pcapng")
    a = '%s|%s' % (res[0].ip.src, res[0].ip.dst)
    print(a)
