from scapy.all import sniff, IP
import psutil
import os
import requests
import json

API_URL = "http://127.0.0.1:5000/predict"  # Your AI model API

# Get the process (application) making the network request
def get_process_name(ip):
    try:
        # Check outgoing connections
        for conn in psutil.net_connections(kind='inet'):
            if conn.raddr and conn.raddr.ip == ip:
                return psutil.Process(conn.pid).name()
        
        # Check listening (incoming) connections
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.laddr.ip == ip:
                return psutil.Process(conn.pid).name()
    
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "Unknown"

    return "Unknown"


# Windows firewall command to block an IP
def block_ip(ip, app_name):
    print(f"🚨 BLOCKING {ip} (App: {app_name}) using Windows Firewall")
    os.system(f'netsh advfirewall firewall add rule name="Blocked {ip}" dir=out action=block remoteip={ip}')

# Function to send packet details to AI model
def analyze_traffic(src_ip, dst_ip, packet_size):
    app_name = get_process_name(dst_ip)

    data = {
        "ip": dst_ip,
        "app": app_name,  # Include application name
        "packet_size": packet_size,
        "request_frequency": 10,  # Example value, can be calculated
        "port": 80  # Default HTTP, can extract dynamically
    }

    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        if result.get("decision") == "block":
            print(f"🚫 AI DECISION: BLOCK {dst_ip} (App: {app_name})")
            block_ip(dst_ip, app_name)
        else:
            print(f"✅ AI DECISION: ALLOW {dst_ip} (App: {app_name})")
    except Exception as e:
        print(f"Error contacting AI model: {e}")

# Function to process each packet
def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        packet_size = len(packet)

        print(f"📡 Checking: {src_ip} -> {dst_ip} (Size: {packet_size})")
        analyze_traffic(src_ip, dst_ip, packet_size)

# Start packet sniffing
print("🔥 AI-Powered Firewall Running... Press CTRL+C to Stop.")
sniff(prn=packet_callback, store=0)
