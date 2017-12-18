from pypacker import ppcap
from pypacker.pypacker import mac_bytes_to_str, mac_str_to_bytes, pack_mac, unpack_mac
from pypacker.layer12 import radiotap, ieee80211, ethernet

# Packet filter class
class PacketFilter:
    """
    Convenience filter combining.
    """
    def __init__(self, fn):
        self.fn = fn
    def __call__(self, *args):
        return self.fn(*args)
    def __and__(self, other):
        l = lambda *args: self.fn(*args) & other(*args)
        return PacketFilter(l)
    def __rand__(self, other):
        return self.__and__(other)
    def __or__(self, other):
        l = lambda *args: self.fn(*args) | other(*args)
        return PacketFilter(l)
    def __ror__(self, other):
        return self.__or__(other)
    def __invert__(self):
        l = lambda *args: ~other(*args)
        return PacketFilter(l)
    def __xor__(self, other):
        l = lambda *args: self.fn(*args) ^ other(*args)
        return PacketFilter(l)
    def __rxor__(self, other):
        return self.__xor__(other)

# Filters
def filter_mac_src(mac):
    mac = mac_str_to_bytes(mac)
    def f(rt):
        curr = rt.upper_layer
        while curr is not None:
            if hasattr(curr, 'src'):
                return curr.src == mac
            curr = curr.upper_layer
        return False
    return PacketFilter(f)

def filter_mac_dest(mac):
    mac = mac_str_to_bytes(mac)
    def f(rt):
        curr = rt.upper_layer
        while curr is not None:
            if hasattr(curr, 'dst'):
                return curr.dst == mac
            curr = curr.upper_layer
        return False
    return PacketFilter(f)

def filter_mac_any(mac):
    mac = mac_str_to_bytes(mac)
    def f(rt):
        curr = rt.upper_layer
        while curr is not None:
            if (hasattr(curr, 'src') and curr.src == mac) or \
               (hasattr(curr, 'dst') and curr.dst == mac):
                return True
            curr = curr.upper_layer
        return False
    return PacketFilter(f)

def filter_mac_one_way(smac, dmac):
    smac = mac_str_to_bytes(smac)
    dmac = mac_str_to_bytes(dmac)
    def f(rt):
        curr = rt.upper_layer
        while curr is not None:
            if hasattr(curr, 'src') and hasattr(curr, 'dst'):
                return curr.src == smac and curr.dst == dmac
            curr = curr.upper_layer
        return False
    return PacketFilter(f)

def filter_mac_two_way(mac1, mac2):
    mac1 = mac_str_to_bytes(mac1)
    mac2 = mac_str_to_bytes(mac2)
    def f(rt):
        curr = rt.upper_layer # radio tap does not have mac
        while curr is not None:
            if hasattr(curr, 'src') and hasattr(curr, 'dst'):
                return (curr.src == mac1 and curr.dst == mac2) or \
                       (curr.src == mac2 and curr.dst == mac1)
            curr = curr.upper_layer
        return False
    return PacketFilter(f)

# Utils
def map_pcap(f, pcap_name, lowest_layer=None, pktfilter=None):
    pcap = ppcap.Reader(pcap_name, lowest_layer=lowest_layer, pktfilter=pktfilter)
    xs, ys = [], []
    bt = None
    for ts, buf in pcap:
        if bt is None: bt = ts
        xs.append((ts - bt)/(60 * 10**9))
        ys.append(f(buf))
    return xs, ys

FRAME_TYPES = [0, 1, 2]
M_TYPES = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 
           0b1000, 0b1001, 0b1010, 0b1011, 0b1100]
C_TYPES = [0b1010, 0b1011, 0b1100, 0b1101, 0b1110, 0b1111]
D_TYPES = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
