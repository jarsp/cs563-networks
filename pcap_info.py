import os

pc_mac = '5c:c5:d4:7d:f1:ae'
android_mac = 'a8:b8:6e:21:6f:54'
router_mac = '00:50:f1:80:00:00'
wemo_mac = '14:91:82:b4:47:0d'
neo_mac = 'b4:43:0d:b9:b9:92'
jinvoo_mac = '60:01:94:34:2f:a5'
ihome_mac = '40:9f:38:18:d7:5f'
dlink_mac = '90:8d:78:e3:79:89'
tplink_mac = '70:4f:57:ff:61:de'
mjerry_mac = '60:01:94:92:b2:4a'
tuya_mac = '60:01:94:92:8d:03'
edimax_mac = '74:da:38:4a:d2:4f'
cevitor_mac = '60:01:94:51:62:7c'
aws_mac = '88:71:e5:a8:9b:a9'
dlsensor_mac = '70:62:b8:93:82:3c'
shsensor_mac = '18:fe:34:dc:7b:eb'
tpldongle_mac = 'c0:25:e9:1b:77:12'

mac_list = [
    wemo_mac,
    neo_mac,
    jinvoo_mac,
    ihome_mac,
    dlink_mac,
    tplink_mac,
    mjerry_mac,
    tuya_mac,
    edimax_mac,
    cevitor_mac,
    #android_mac,
    shsensor_mac,
    dlsensor_mac,
    aws_mac,
    tpldongle_mac
]

pcap_dir = './captures'

device_list = ['wemo', 'neo', 'jinvoo', 'ihome', 'dlink', 'tplink', 'mjerry', 'tuya',
               'edimax', 'cevitor']
#non_switch = ['android', 'shsensor', 'dlsensor', 'aws']
non_switch = ['shsensor', 'dlsensor', 'aws']
non_actuated = ['pc']
actuated_device_list = device_list + non_switch
all_device_list = actuated_device_list + non_actuated

experiments = ['qswitch', 'qoff_app', 'qoff_noapp', 'qon_app', 'qon_noapp']

pcaps = {}
for dev in actuated_device_list:
    pcaps[dev] = [os.path.join(pcap_dir, dev,
                              '{}_qswitch.pcap'.format(dev))]

pcaps['pc'] = [os.path.join(pcap_dir, 'pc/browsing_video.pcap')]

# Frame type info
frame_types = {i:'Unknown/Reserved' for i in range(64)}

frame_types[0b000000] = 'Management - Association Request'
frame_types[0b000100] = 'Management - Association Response'
frame_types[0b001000] = 'Management - Re-Association Request'
frame_types[0b001100] = 'Management - Re-Association Response'
frame_types[0b010000] = 'Management - Probe Request'
frame_types[0b010100] = 'Management - Probe Response'
frame_types[0b011000] = 'Management - Timing Advertisement'
frame_types[0b011100] = 'Management - Reserved'
frame_types[0b100000] = 'Management - Beacon'
frame_types[0b100100] = 'Management - ATIM'
frame_types[0b101000] = 'Management - Disassociation'
frame_types[0b101100] = 'Management - Authentication'
frame_types[0b110000] = 'Management - Deauthentication'
frame_types[0b110100] = 'Management - Action'
frame_types[0b111000] = 'Management - Action no Ack'
frame_types[0b111100] = 'Management - Reserved'

frame_types[0b011101] = 'Control - Control Wrapper'
frame_types[0b100001] = 'Control - Block Ack Request'
frame_types[0b100101] = 'Control - Block Ack'
frame_types[0b101001] = 'Control - PS-Poll'
frame_types[0b101101] = 'Control - RTS'
frame_types[0b110001] = 'Control - CTS'
frame_types[0b110101] = 'Control - ACK'
frame_types[0b111001] = 'Control - CF-End'
frame_types[0b111101] = 'Control - CF-End + CF-Ack'

frame_types[0b000010] = 'Data - Data'
frame_types[0b000110] = 'Data - Data + CF-Ack'
frame_types[0b001010] = 'Data - Data + CF-Poll'
frame_types[0b001110] = 'Data - Data + CF-Ack + CF-Poll'
frame_types[0b010010] = 'Data - Null'
frame_types[0b010110] = 'Data - CF-Ack'
frame_types[0b011010] = 'Data - CF-Poll'
frame_types[0b011110] = 'Data - CF-Ack + CF-Poll'
frame_types[0b100010] = 'Data - QoS Data'
frame_types[0b100110] = 'Data - QoS Data + CF-Ack'
frame_types[0b101010] = 'Data - QoS Data + CF-Poll'
frame_types[0b101110] = 'Data - QoS Data + CF-Ack + CF-Poll'
frame_types[0b110010] = 'Data - QoS Null'
frame_types[0b110110] = 'Data - Reserved'
frame_types[0b111010] = 'Data - QoS CF-Poll'
frame_types[0b111110] = 'Data - QoS CF-Ack + CF-Poll'

