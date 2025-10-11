import socket
import json
import subprocess
import re

lamp_mac = "cc-40-85-78-e3-4a"
lamp_mac = lamp_mac.lower()  # Preprocessing
lamp_ip = None
lamp_port = 38899

# List all the ips in the local wireless network with "arp -a"
result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
arp_out = result.stdout

for line in arp_out.splitlines():
    if lamp_mac in line.lower():
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
        if match:
            lamp_ip = match.group(1)
            print("Lamp IP found:", lamp_ip)

if lamp_ip is not None:
    transmit_ip = lamp_ip
    print("IP Status: Direct lamp transmission")
else:
    transmit_ip = "192.168.1.255"
    print("IP Status: Broadcast transmission")

# msg = {"method": "setPilot", "params": {"state": True}}  # ON
msg = {"method": "setPilot", "params": {"state": False}}  # OFF
# msg = {"method":"setPilot","params":{"dimming":100}}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(msg).encode(), (transmit_ip, lamp_port))
print("Command sent!")