#!/usr/local/bin/python3.6

import os
from Crypto.Hash import SHA256

def read_video():
    divisor = 1024
    end = os.stat("/home/ciunas/6.1.intro.mp4_download").st_size % divisor
    with open("/home/ciunas/6.1.intro.mp4_download", "rb") as infile:
        data = infile.read()
        hash = sha256(data[len(data)-end:len(data)])
        for i in range(len(data)-end, 0, divisor*-1):
            hash = sha256(data[i-divisor:i] + hash)
            print (hash.hex())
    return  hash.hex()

def sha256(bytes):
    h = SHA256.new()
    h.update(bytes)
    return h.digest()

print (read_video())
