import matplotlib.pyplot as plt

from Core.ReadPcap import ReadPcap
from Stream.StreamExtractor import StreamExtractor

from Util.StatisticTools import describe

# 解析pcap文件，获得数据列表
path = "C:\\Users\\Hikari\\Desktop\\ipsec\\本地ipsec1000.pcapng                                                        "
packet_list = ReadPcap(path)

stream_ext = StreamExtractor(packet_list)

stream_list = stream_ext.ex_tcp_stream()

stream = stream_list[1]

pkt_size = stream.pkt_size()

print(describe(pkt_size))

# 报文大小分布直方图
pkt_size.hist(grid=True, bins=50, rwidth=0.9).plot()
plt.show()
