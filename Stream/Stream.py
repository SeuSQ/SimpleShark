import numpy as np
import pandas as pd


class Stream:
    def __init__(self, stream_id, side_a, side_b, plist, direct=None):
        self.stream_id = stream_id
        self.side_a = side_a
        self.side_b = side_b
        self.packets = plist
        self.direct = direct
        self._pkt_size_list = None
        self._pkt_time_list = None

    # 报文长度列表
    def pkt_size(self):
        if self._pkt_size_list is not None:
            return np.array(self._pkt_size_list)
        self._pkt_size_list = []
        for p in self.packets:
            self._pkt_size_list.append(p.length)
        return pd.Series(self._pkt_size_list).astype('int')

    # 报文到达间隔列表
    def pkt_iat(self):
        if self._pkt_time_list is not None:
            return np.diff(np.array(self._pkt_time_list))
        self._pkt_time_list = []
        for p in self.packets:
            self._pkt_time_list.append(p.time)
        return np.diff(np.array(self._pkt_time_list))

    # 报文到达速率（报文数）
    def pkt_num_rate(self, interval=1000):
        self._make_pkt_list()
        num = len(self.packets)
        pkt_se = pd.Series([1]*num, index=self._pkt_time_list)
        pkt_se.astype('int')
        res = pkt_se.resample(str(interval)+'L').sum()
        return res

    # 报文到达速率（Bytes）
    def pkt_bytes_rate(self, interval=1000):
        self._make_pkt_list()
        pkt_se = pd.Series(self._pkt_size_list, index=self._pkt_time_list)
        pkt_se.astype('int')
        res = pkt_se.resample(str(interval)+'L').sum()
        return res

    def _make_pkt_list(self):
        if self._pkt_size_list is None:
            self._pkt_size_list = []
            for p in self.packets:
                self._pkt_size_list.append(int(p.length))
        if self._pkt_time_list is None:
            self._pkt_time_list = []
            for p in self.packets:
                self._pkt_time_list.append(p.time)

    def pkt_index_size(self):
        self._make_pkt_list()
        return pd.Series(self._pkt_size_list, index=self._pkt_time_list)
