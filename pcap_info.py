import os

pc_mac = '5c:c5:d4:7d:f1:ae'
android_mac = 'a8:b8:6e:21:6f:54'
router_mac = '00:50:f1:80:00:00'
wemo_mac = '14:91:82:b4:47:0d'
neo_mac = 'b4:43:0d:b9:b9:92'
hikenri_mac = '60:01:94:34:2f:a5'
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

mac_list = [
    wemo_mac,
    neo_mac,
    hikenri_mac,
    ihome_mac,
    dlink_mac,
    tplink_mac,
    mjerry_mac,
    tuya_mac,
    edimax_mac,
    cevitor_mac,
    pc_mac,
    android_mac,
    shsensor_mac,
    dlsensor_mac,
    aws_mac
]

pcap_dir = '../pcap/switching'

device_list = ['wemo', 'neo', 'hikenri', 'ihome', 'dlink', 'tplink', 'mjerry', 'tuya',
               'edimax', 'cevitor']
no_radiotap = ['tplink', 'mjerry', 'tuya']
non_switch = ['pc', 'android', 'shsensor', 'dlsensor', 'aws']
all_device_list = device_list + non_switch
experiments = ['qswitch', 'qoff_app', 'qoff_noapp', 'qon_app', 'qon_noapp']
pcaps = {}
for dev in device_list:
    pcaps[dev] = [os.path.join(pcap_dir, dev,
                               '{}_{}.pcap'.format(dev, exp))
                  for exp in experiments]

pcaps_switching = {}
for dev in device_list:
    pcaps_switching[dev] = [os.path.join(pcap_dir, dev,
                                        '{}_qswitch.pcap'.format(dev))]

pcaps['pc'] = [os.path.join(pcap_dir, 'pc_browsing.pcap')]
pcaps['android'] = [os.path.join(pcap_dir, 'android_browsing.pcap')]

pcaps_switching['pc'] = [os.path.join(pcap_dir, 'pc_browsing.pcap')]
pcaps_switching['android'] = [os.path.join(pcap_dir, 'android_browsing.pcap')]
pcaps_switching['shsensor'] = [os.path.join(pcap_dir, 'shsensor', 'shsensor_qswitch.pcap')]
pcaps_switching['dlsensor'] = [os.path.join(pcap_dir, 'dlsensor', 'dlsensor_qswitch.pcap')]
pcaps_switching['aws'] = [os.path.join(pcap_dir, 'aws', 'aws_qswitch.pcap')]
