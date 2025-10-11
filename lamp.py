import socket
import json
import subprocess
import re
from time import sleep

class WiZLampUDS():
    wiz_port = 38899  # Fixed port for WiZ devices
    def __init__(self):
        self.lamp_ip = None
        self.lamp_mac = "cc-40-85-78-e3-4a"

    def set_ip(self, lamp_ip: str):
        self.lamp_ip = lamp_ip

    def set_mac(self, lamp_mac:str):
        self.lamp_mac = lamp_mac.lower()

    def set_ip_from_mac(self):
        """
        :param lamp_mac: MAC Address of the lamp, e.g. "cc-40-85-78-e3-4a"
        """
        search_ip = None
        # List all the ips in the local wireless network with "arp -a"
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        arp_out = result.stdout

        for line in arp_out.splitlines():
            if self.lamp_mac in line.lower():
                match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if match:
                    search_ip = match.group(1)
                    

        if search_ip is not None:
            self.lamp_ip = search_ip
            print("IP from MAC Address", self.lamp_ip)
        else:
            print("No response")
            self.lamp_ip = None
        
        return bool(search_ip is not None)

    def query_ip_from_lamp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(2)
        msg = {"method": "getSystemConfig", "params": {}}
        sock.sendto(json.dumps(msg).encode(), ("255.255.255.255", self.wiz_port))
        try:
            data, addr = sock.recvfrom(1024)
            self.lamp_ip = addr[0]
            print("IP from Broadcast Lamp Query:", self.lamp_ip)
        except socket.timeout:
            self.lamp_ip = None
            print("No response")
        sock.close()
        return bool(self.lamp_ip is not None)
    
    def search_ip(self):
        if(self.query_ip_from_lamp() is False):
            if(self.set_ip_from_mac() is False):
                print("Could not configure IP, IP set to broadcast")
                self.lamp_ip = "192.168.1.255"
                

    def send_uds_command(self, params: dict):
        """
        :param params: e.g. {"dimming": 10}
        """
        msg = {"method": "setPilot", "params": params}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(msg).encode(), (self.lamp_ip, self.wiz_port))
        print(f"Sent command: {params}")
        sock.close()

if __name__ == "__main__":
    # Start main application
    wiz_lamp = WiZLampUDS()
    # wiz_lamp.set_ip_from_mac("cc-40-85-78-e3-4a")
    # wiz_lamp.send_uds_command({"state": False})
    # wiz_lamp.send_uds_command({"state": True})
    wiz_lamp.search_ip()