# Annual Project: Bad USB Attack Framework

This project details the development of a "Bad USB" solution designed to automate the initial stages of a penetration test, specifically focusing on payload delivery, command and control (C2) establishment, privilege escalation, and persistence.

Disclaimer: This project is developed for educational purposes only, to understand and demonstrate cybersecurity attack vectors. It should never be used on systems without explicit, written permission from the owner. Unauthorized use of this software is illegal and unethical. The developer assumes no responsibility for any misuse or damage caused by this project.

# 🚀 Features
### Bad USB Payload Injection: 
Utilizes a Bad USB device to automatically input a wget command, retrieving the C2 client onto the target system.

### Automated C2 Client Execution: 
Immediately launches the downloaded C2 client upon successful transfer.

### Privilege Escalation: 
Leverages the **CVE-2025-6019** CVE to achieve root privileges on the compromised system.

### Persistent C2 Connection: 
Establishes persistence by creating a systemd service, ensuring the C2 client restarts with the system and runs as root.

### Server-Side Logging: 
The C2 server logs all relevant attack data and interactions into /etc/attack.txt on the server machine.

# 🛠️ How it Works
The workflow of this attack framework is orchestrated in several stages:

- ### Initial Access (Bad USB):

A Bad USB device, when plugged into a target machine, emulates a keyboard.

It executes a pre-programmed payload (a wget command) to download the C2 client from the attacker's server.

Once downloaded, the Bad USB script automatically executes the client.

- ### Command & Control (C2) Client:

The client establishes a connection back to the attacker's C2 server.

It is designed to be lightweight and facilitate remote command execution.

- ###  Privilege Escalation:

Upon connecting to the server, the C2 client (or a component initiated by it) exploits the **CVE-2025-6019** CVE to elevate its privileges to root.

The CVE is explained [here](https://ubuntu.com/security/CVE-2025-6019)

- ###  Persistence:

After gaining root access, the C2 client writes a systemd service file to the target system.

This service ensures that the C2 client automatically starts with root privileges every time the system boots, maintaining persistent access for the attacker.

- ###  Server-Side Monitoring & Logging:

The C2 server acts as the central hub, receiving connections and commands from compromised clients.

All interactions, executed commands, and system information gathered are meticulously logged into a file located at /etc/attack.txt on the server. This provides a comprehensive record of the attack.

## 📂 Project Structure
```
├── Base-C2
│   ├── client.py
│   ├── readme
│   └── server.py
├── C2-attack.sh
└── contact.py
```

 ## ⚙️ Setup and Installation
To leverage the BadUSB into a root C2, we need a XFS image with a bash inside.

All of this commands needs to be done in root, in the root of the repository, and it should be done by the same architecture (e.g. x64) as the target

    dd if=/dev/zero of=./xfs.image bs=1M count=300

    mkfs.xfs ./xfs.image

    mkdir ./xfs.mount

    mount -t xfs ./xfs.image ./xfs.mount

    cp /bin/bash ./xfs.mount

    chmod 04555 ./xfs.mount/bash

    umount ./xfs.mount

#### 1. Bad USB Device Preparation
Obtain a programmable Bad USB device (e.g., Rubber Ducky, Digispark, Raspberry Pico).

Make sure all the file for a BadUSB are there

#### 2. C2 Server Setup
Clone this repository to your server:

Right now, The server needs to be in the same network as the target. 

⚠️ **I will not explain here how to make the client accessible when the server is not in the same network.** ⚠️

Verify the server has write permissions to /etc/attack.txt

## 🚀 Usage

    sh C2-attack.sh MOUNT_POINT

Start the C2 Server:

# Example of an attack on a linux machine

- Plug in your BadUSB (in safe mode) and mount it (e.g. ***/mnt***)
```
sudo mount /dev/sdaX /mnt
```

- Launch the script with your mount directory in argument
```
sh C2-attack.sh /mnt
```

- It will tell you when you can remove the BadUSB (it automatically unmount it)
```
BadUSB payload written to /mnt/payload.dd. Please safely remove the USB drive
```

- It will then start the python server that will transfer the client_r.py. From now on, you need to plug in the BadUSB to your target, while logged in.

- The script will start, opening a terminal and executing the payload. It will then connect to the python server, download the client_r.py and execute it.

If you followed every steps, you should start to see a new connexion on the CLI of the C2 server.

**Have fun !**

## 🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License.
