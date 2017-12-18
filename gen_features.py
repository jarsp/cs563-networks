import numpy as np
import os
import sys

from collections import deque
from itertools import chain

from pypacker import ppcap
from pypacker.pypacker import mac_bytes_to_str, mac_str_to_bytes, pack_mac, unpack_mac
from pypacker.layer12 import radiotap, ieee80211, ethernet

from utils import *
from pcap_info import *

def pkt_slice_pcap(pcap, window, step):
    assert window > step
    assert step >= 1

    buf = []
    for i in range(window):
        buf.append(pcap._next_packet())
    while True:
        yield list(buf) # yields a copy
        for i in range(step):
            buf.append(pcap._next_packet())
        buf = buf[step:]

TS_SCALE = 1000000000
def time_slice_pcap(pcap, window, step):
    assert window > step
    assert step >= 1

    curr_window, window_buf = pcap._next_packet()
    curr_window /= TS_SCALE
    window_buf = deque([(curr_window, window_buf)])

    curr_step = curr_window
    next_step_ind = 1
    step_inds = deque()

    # Windows are half-open on the right
    for ts, buf in pcap:
        # Precondition: curr_step \in [curr_window, curr_window + window)
        ts /= TS_SCALE

        # Record steps until ts in step
        ts_prestep = ts - step
        while curr_step <= ts_prestep:
            curr_step += step
            step_inds.append(next_step_ind)
            next_step_ind = 0

        # Step window and yield until ts in window
        ts_prewindow = ts - window
        while curr_window <= ts_prewindow:
            yield curr_window, curr_window + window, list(window_buf)
            for i in range(step_inds.popleft()):
                window_buf.popleft()
            curr_window += step

        window_buf.append((ts/TS_SCALE, buf))
        next_step_ind += 1

        # Postcondition: ts \in [curr_window, curr_window + window)

    # Yield remaining packets
    if len(window_buf) != 0:
        yield curr_window, curr_window + window, list(window_buf)

def gen_samples(pcap_name, mac, window=25, step=1, is_time_slice=True, has_radiotap=True):
    pktfilter = filter_mac_any(mac)
    if has_radiotap:
        pcap = ppcap.Reader(pcap_name, lowest_layer=radiotap.Radiotap,
                            pktfilter=pktfilter)
    else:
        pcap = ppcap.Reader(pcap_name, lowest_layer=ieee80211.IEEE80211,
                            pktfilter=pktfilter)

    if is_time_slice:
        return time_slice_pcap(pcap, window, step)
    else:
        return pkt_slice_pcap(pcap, window, step)

# TODO: Make more modular
def extract_features(mac, ws, we, data, has_radiotap=True):
    mac_bytes = mac_str_to_bytes(mac)
    w = we - ws
    ctot_num = np.zeros(1)
    ctot_sz = np.zeros(1)
    stot_num = np.zeros(1)
    stot_sz = np.zeros(1)
    l2tot_sz = np.zeros(1)
    ct_num = np.zeros(3)
    ct_sz = np.zeros(3)
    st_num = np.zeros(3)
    st_sz = np.zeros(3)
    l2t_sz = np.zeros(3)
    c_num = np.zeros(64)
    c_sz = np.zeros(64)
    s_num = np.zeros(64)
    s_sz = np.zeros(64)

    for ts, pkt in data:
        try:
            ieee = pkt.ieee80211 if has_radiotap else pkt
        except:
            continue
        l = len(ieee)
        ll = l*l
        tp = ieee.type
        stp = (ieee.subtype << 2) | ieee.type

        ctot_num += 1
        ct_num[tp] += 1
        c_num[stp] += 1

        ctot_sz += l
        ct_sz[tp] += l
        c_sz[stp] += l

        if hasattr(ieee.upper_layer, 'src') and ieee.upper_layer.src == mac_bytes:
            stot_num += 1
            st_num[tp] += 1
            s_num[stp] += 1

            stot_sz += l
            st_sz[tp] += l
            s_sz[stp] += l

    ratetot_num = ctot_num/w
    ratetot_sz = ctot_sz/w
    ratet_num = ct_num/w
    ratet_sz = ct_sz/w
    rate_num = c_num/w
    rate_sz = c_sz/w

    fract_num = ct_num/ctot_num
    fract_sz = ct_sz/ctot_sz
    frac_num = c_num/ctot_num
    frac_sz = c_sz/ctot_sz

    # Use stot_num, stot_sz somewhere?
    sratt_num = st_num/ct_num
    sratt_sz = st_sz/ct_sz
    srat_num = s_num/c_num
    srat_sz = s_sz/c_sz

    ltot_sz = ctot_sz/ctot_num
    lt_sz = ct_sz/ct_num
    l_sz = c_sz/c_num

    sdtot_sz = np.zeros(1)
    sdt_sz = np.zeros(3)
    sd_sz = np.zeros(64)

    for ts, pkt in data:
        try:
            ieee = pkt.ieee80211 if has_radiotap else pkt
        except:
            continue
        l = len(ieee)
        tp = ieee.type
        stp = (ieee.subtype << 2) | ieee.type

        sdtot_sz += (l - ltot_sz) ** 2
        sdt_sz[tp] += (l - lt_sz[tp]) ** 2
        sd_sz[stp] += (l - l_sz[stp]) ** 2

    sdtot_sz = np.sqrt(sdtot_sz/(ctot_num - 1))
    sdt_sz = np.sqrt(sdt_sz/(ct_num - 1))
    sd_sz = np.sqrt(sd_sz/(c_num - 1))

    vec = list(map(np.nan_to_num,
                   chain(ratetot_num, ratetot_sz, ratet_num, ratet_sz, rate_num, rate_sz,
                         fract_num, fract_sz, frac_num, frac_sz,
                         sratt_num, sratt_sz, srat_num, srat_sz,
                         ltot_sz, lt_sz, l_sz,
                         sdtot_sz, sdt_sz, sd_sz)))

    return vec

# TODO: use np.save and load in future
if __name__ == '__main__':
    # for i, (dev, mac) in enumerate(zip(all_device_list, mac_list)):
    #     for pcap_file in pcaps_switching[dev]:
    #         with open('{}/{}.txt'.format(sys.argv[1], os.path.basename(pcap_file)), 'w+') as f:
    #             s = ''
    #             has_rt = dev not in no_radiotap
    #             for tup in gen_samples(pcap_file, mac, has_radiotap=has_rt):
    #                 v = map(str, extract_features(mac, *tup, has_radiotap=has_rt))
    #                 s += str(i) + ' ' + ' '.join(v) + '\n'
    #             f.write(s)
    
    fn = './captures/cevitor/cevitor_qswitch.pcap'
    # pktfilter = filter_mac_any(cevitor_mac)
    pcap = ppcap.Reader(fn, lowest_layer=radiotap.Radiotap)
    for ts, data in pcap:
        print(data.ieee80211.upper_layer.src_s, data.ieee80211.upper_layer.dst_s)
    
