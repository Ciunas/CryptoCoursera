#!/usr/local/bin/python3.6

import urllib.response, urllib.parse, urllib.request
import sys

queryString = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
queryBytes = bytes.fromhex(queryString)

TARGET = 'http://crypto-class.appspot.com/po?er='

def query(string):
    target = TARGET + urllib.parse.quote(string)    # Create query URL
    req = urllib.request.Request(target)         # Send HTTP request to server
    try:
        f = urllib.request.urlopen(req)          # Wait for response
    except urllib.error.HTTPError as e:          
        print ("We got: %d" % e.code)       # Print response code
        if e.code == 404:
            return True # good padding
        return False # bad padding

def changeQueryByte(ct):
    dt = b''
    for i, j in  zip(range(1, 17, 1), range(31,15,-1)):
        xor = (i).to_bytes(1, byteorder='big') * i
        print (ct.hex())
        for k in range(0,256):
           g = (k).to_bytes(1, byteorder='big')
           temp1 = bxor(g, ct[j:j+1] )
           temp2 = bxor(temp1, xor)
           nt = ct[0:j] + temp2 + ct[j+1:len(ct)]
           print(nt.hex())
           if query(nt.hex()) == True:
               dt = g + dt
               ct = ct[0:16] + changeCT(dt, ct[16:32], i) + ct[32:len(ct)]
               print (dt)
               break
    return dt

def changeCT(byteValue, ct, byteNum):
    print (len(ct))
    ct = ct[0:len(ct)-byteNum]
    tt =  queryBytes[32-byteNum:32]
    print (ct.hex())
    print (tt.hex())
    for i in range(0, len(byteValue)):
        print (i)
        temp = bxor(tt[i:i+1], byteValue[i:i+1])
        print(temp.hex())
        ct = ct +  bxor(temp, (len(byteValue)+1).to_bytes(1, byteorder='big') )
    print(ct.hex())
    return ct
    
def bxor(b1, b2): # returns xor of byte(s) b1 and b2
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)
print (len(queryBytes))
print (queryBytes)
result = b''
result = changeQueryByte(queryBytes[16:64])
print (result)
result = changeQueryByte(queryBytes[0:48]) + result 
print (result)
result = changeQueryByte((b'0'*16) + queryBytes[0:32]) + result 
print ( result )
