import psutil
import socket
import requests
import os

API_URL = "http://127.0.0.1:5000/predict"  # Your AI model API

def get_active_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_ESTABLISHED:
            try:
                process = psutil.Process(conn.pid)
                app_name = process.name()
                remote_ip = conn.raddr.ip if conn.raddr else None
                port = conn.raddr.port if conn.raddr else None
                packet_size = 1024  # Example size, real-time tracking needs monitoring

                if remote_ip:
                    connections.append((app_name, remote_ip, port, packet_size))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    return connections

def analyze_traffic(app_name, ip, port, packet_size):
    data = {
        "ip": ip,
        "packet_size": packet_size,
        "request_frequency": 10,  # Example, can be dynamically updated
        "port": port
    }

    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        decision = result.get("decision", "allow")

        print(f"📡 App: {app_name}, IP: {ip}, Port: {port} -> {decision.upper()}")

        if decision == "block":
            block_ip(ip)
    except Exception as e:
        print(f"❌ Error contacting AI model: {e}")

def block_ip(ip):
    print(f"🚨 BLOCKING {ip} using Windows Firewall")
    os.system(f'netsh advfirewall firewall add rule name="Blocked {ip}" dir=out action=block remoteip={ip}')

if __name__ == "__main__":
    print("🔥 Application Tracker Running...")
    while True:
        connections = get_active_connections()
        for app, ip, port, size in connections:
            analyze_traffic(app, ip, port, size)
