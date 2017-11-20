#!/usr/bin/python3.4

import gmpy2
import time

start = time.time()
p = gmpy2.mpz('134078079299425970995740249982058461274793658205923933777235614437217640300'
    '73546976801874298166903427690031858186486050853753882811946569946433649006084171')

g = gmpy2.mpz('117178298803662070095161175963353670885580849999989522055999794590639294997'
    '36583746670572176471460312928594829675428279466566527115212748467589894601965568')

h = gmpy2.mpz('323947510405045044356526437872806578864909752095244952783479245297198197614'
    '3292558073856937958553180532878928001494706097394108577585732452307673444020333')

B = gmpy2.mpz(2 ** 20)
LHS= {}

def computeLHS():
    for i in range(0, B):
        gx1 = gmpy2.divm(h, gmpy2.powmod(g, i, p), p) #calculat g pow i mod p for range 0-B
        try:
            LHS[gx1] = LHS[gx1] + i
        except Exception:
            LHS[gx1] = i
    print ("Finished LHS")
    return

def computeRHSandCompare():
    for i in range(0, B):
        RHS = gmpy2.powmod(g, i*B, p)
        if RHS in  LHS:
            x = i * B + LHS.get(RHS)
            print ("Value Found")
            print (x)
            return
computeLHS()
computeRHSandCompare()
print (time.time() - start)
