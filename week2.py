#!/usr/local/bin/python3.6

from Crypto.Cipher import AES

unpad = lambda s : s[0:-s[-1]]
cbc_key = bytes.fromhex('140b41b22a29beb4061bda66b6747e14')
ctr_key = bytes.fromhex('36f18357be4dbd77f050515c73fcf9f2')
cbc_cipher_1 = bytes.fromhex('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad078'\
        '83d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81')
cbc_cipher_2 = bytes.fromhex('5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7d'\
        'a33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df455034'\
        '73c5242a253')
ctr_cipher_1 = bytes.fromhex('69dda8455c7dd4254bf353b773304eec0ec7702330098ce7'\
        'f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97e'\
        'f79d59ce29f5f51eeca32eabedd9afa9329')
ctr_cipher_2 = bytes.fromhex('770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca6'\
        '95ae45faa8952aa0e311bde9d4e01726d3184c34451')
msg = bytes.fromhex('426173696320434243206d6f646520656e6372797074696f6e206e6565'\
        '64732070616464696e672e')
pt1 = b'Basic CBC mode encryption needs padding.'
pt2 = b'Our implementation uses rand. IV'

def encrypt_cbc(key, pt):
    iv = cbc_cipher_1[:16]
    istblock = bxor(iv, pt[:16])
    cipher = AES.new(key, AES.MODE_ECB)
    ct = iv  + cipher.encrypt(istblock)
    for i in range(16, len(pt)-15, 16):
        nextblock =  bxor(ct[i:i+16], pt[i:i+16])
        ct +=  cipher.encrypt(nextblock)
    pad = len(pt) % 16
    if(pad == 0):
        pad  = 16
    nextblock =  bxor(ct[len(ct)-16:len(ct)], pt[len(pt)-len(pt) % 16:len(pt)] + bytes([pad])*pad)
    ct += cipher.encrypt(nextblock)
    return ct.hex()

def decrypt_cbc(key, ct ):
        iv = ct[:16]
        ct = ct[16:]
        cipher = AES.new(key, AES.MODE_ECB)
        c0 = cipher.decrypt( ct[0:16])
        pt = bxor(iv, c0)
        for i in range(16, len(ct)-15, 16):
            c1 = cipher.decrypt(ct[i:i+16])
            pt += bxor(ct[i-16:i], c1)
        return unpad(pt)

def bxor(b1, b2): # returns xor of byte(s) b1 and b2
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)

def decrypt_ctr(key, ct):
    iv =  ct[0:16]
    ct = ct[16:]
    cipher = AES.new(key, AES.MODE_ECB)
    f = cipher.encrypt(iv)
    for i in range(16, len(ct), 16):
         ctr = int.from_bytes(iv, byteorder='big') + 1
         iv = ctr.to_bytes(16, byteorder='big')
         f += cipher.encrypt(iv)
    pt = bxor(f, ct)    
    return pt

def encrypt_ctr(key, pt, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    f = cipher.encrypt(iv)
    ct = iv
    for i in range(16, len(pt), 16):
         ctr = int.from_bytes(iv, byteorder='big') + 1
         iv = ctr.to_bytes(16, byteorder='big')
         f += cipher.encrypt(iv)
    ct += bxor(f, pt)
    return ct.hex()


#print (decrypt_cbc(cbc_key, cbc_cipher_1))
#print (decrypt_cbc(cbc_key, cbc_cipher_2))
print (decrypt_ctr(ctr_key, ctr_cipher_1))
print (decrypt_ctr(ctr_key, ctr_cipher_2))
print (encrypt_ctr(ctr_key, b'CTR mode lets you build a stream cipher from a block cipher.', ctr_cipher_1[0:16]))
print (encrypt_ctr(ctr_key, b'Always avoid the two time pad!', ctr_cipher_2[0:16]))
