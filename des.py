import random
from destables import *


def keygen():
	# generates a 64 bit random key
	key = "" #key in bits
	keyStr = "" #key in str
	for i in range(8):
		keyStr += chr(random.randint(ord('a'), ord('z')))
		key += "{:08b}".format( ord(keyStr[i]) )
	return ( key , keyStr) 


def msgInBinary(msg):
	# transforms the msg into 64 bit pairs
	mb = "".join( ["{:08b}".format(ord(m)) for m in msg] )
	if len(mb)%64 != 0:
		mb += "0"*(64 - len(mb)%64)
	return mb


def rearrange(bits, table):
	# retrieves bits at specific position
	new = ""
	for t in table:
		new += bits[t-1]
	return new


def lshift(bits, n):
	#left shifts the bit by n
	return bits[n:] + bits[:n]

def genKeySet(k1, k2):
	keySet = []
	for i in ls:
		k1 = lshift(k1, i)
		k2 = lshift(k2, i)
		k = rearrange(k1 + k2, p2)
		keySet.append(k)
	return keySet

#slices mb in n groups
slice = lambda mb, n:  [ mb[i:i+n] for i in range(0, n*(len(mb)//n) + 1, n ) ][:-1]
#xor two binary strings
xor = lambda s1, s2: "".join([str(int(a) ^ int(b) )for a,b in zip(s1,s2)])

read = lambda mb: "".join([chr(int(s, 2)) for s in slice(mb,8)])

def encrypt(mb, keySet):
	#encrypts 64 bit pairs of msg
	mbl = slice(mb, 64) #slicing msgbit bits in 64 bi chunks	
	em = ""
	ki = 0
	for i in mbl:
		(l, r) = (i[:32],i[32:])
		previousl = l
		l = r
		r = xor(previousl , f(r, keySet[ki]) )
		em += rearrange(l + r , IP)
		print(em)
		ki += 1
	print(read(em))


def f(r , key):
	r = rearrange(r, E)
	new = ""
	temprl = slice(xor(r,key), 6)
	ri = 0
	for i in temprl:
		row = int( i[0] + i[5] , 2)
		col = int( i[1:5] , 2)
		new += "{:04b}".format(S[ri][row][col])
		ri += 1
	return new


msg = input("\n\nGimme something to encrypt: ")
#key = keygen(msg)
#msg = "himasnhu"


if __name__ == '__main__':
	(k, ks) = keygen()
	mb = msgInBinary(msg)
	ksn = rearrange(k, p1)
	(k1 , k2) = ( ksn[:28] , ksn[28:] )
	keySet = genKeySet(k1, k2)
	encrypt(mb , keySet)
