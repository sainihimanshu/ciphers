import random
from destables import *

#slices 'mb' bit pattern each having 'n' elements
slice = lambda mb, n:  [ mb[i:i+n] for i in range(0, n*(len(mb)//n) + 1, n ) ][:-1]

#xor two binary strings 's1' and 's2'
xor = lambda s1, s2: "".join([str(int(a) ^ int(b) )for a,b in zip(s1,s2)])

#parses bit string 'mb' as a ascii string
read = lambda mb: "".join([chr(int(s, 2)) for s in slice(mb,8)])

#decrypts 64 bit pairs of ciphered text by applying keyset in reverse order
decrypt = lambda ct, keySet: encrypt(ct, list(reversed(keySet)))
	 
#left shifts the 'bits' string by 'n' position
lshift = lambda bits, n: bits[n:] + bits[:n] 

# permutes 'bits' according to the 'table' list and returns the permuted string
rearrange = lambda bits, table: "".join(bits[t-1] for t in table)
		
#Key related functions
def keygen():
	# generates a 64 bit random key and returns it in bit and string format
	key = "" #key in bits
	keyStr = "" #key in str
	for i in range(8):
		keyStr += chr(random.randint(ord('a'), ord('z')))
		key += "{:08b}".format( ord(keyStr[i]) )
	return ( key , keyStr) 


def genKeySet(ksn):
	#returns a list of 16 keys
	(k1 , k2) = ( ksn[:28] , ksn[28:] )
	keySet = []
	for i in ls:
		(k1 , k2) = (lshift(k1, i) , lshift(k2, i) )		
		k = rearrange(k1 + k2, p2)
		keySet.append(k)
	return keySet


#msg related functions
def msgInBinary(msg):
	# transforms the msg into 64 bit pairs 
	#0's are padded if the bits of string is not a multiple of 64 
	mb = "".join( ["{:08b}".format(ord(m)) for m in msg] )
	if len(mb)%64 != 0:
		mb += "0"*(64 - len(mb)%64)
	return mb


def encrypt(mb, keySet):
	#encrypts 64 bit pairs of msg
	mbl = slice(mb, 64) #slicing msgbit bits in 64 bi chunks	
	em = ""
	for i in mbl:
		i = rearrange(i, pm)
		(l, r) = (i[:32],i[32:])
		for k in keySet:
			previousl = l
			l = r
			r = xor(previousl , f(r, k) )
		em += rearrange( r + l , IP)
	return em


def f(r , key):
	# function used in transformation of rn-1 to rn
	r = rearrange(r, E)
	new = ""
	temprl = slice(xor(r,key), 6)
	ri = 0
	for i in temprl:
		row = int( i[0] + i[5] , 2)
		col = int( i[1:5] , 2)
		new += "{:04b}".format(S[ri][row][col])
		ri += 1
	return rearrange(new, P)

def run_des():
	msg = input("\n\nGimme something to encrypt: ")
	#msg = "himanshu"
	(k, ks) = keygen()
	mb = msgInBinary(msg)
	ksn = rearrange(k, p1) #64 to 56
	keySet = genKeySet(ksn)
	em = encrypt(mb , keySet)
	print("hi")
	print("Generated key: " + ks + "\nEncrypted text: " + read(em))
	print("Decrypted text: " + read(decrypt(em, keySet)) )

if __name__ == '__main__':
	run_des()