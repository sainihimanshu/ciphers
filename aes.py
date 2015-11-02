#generating key
from random import *
from aestables import *

tohex = lambda num: "{:02x}".format(num) #converts an int to a hex 
toint = lambda x: int(str(x) , base = 16) #converts an hex to an int
 
key = [tohex(choice(range(ord("A"), ord("Z") ))) for i in range(16) ] #16 random alphabets

shift = lambda i: i[1:] + [i[0]] #left circular shift

xor = lambda x1, x2: tohex(toint(x1) ^ toint(x2) )

slice = lambda mx, n:  [ mx[i:i+n] for i in range(0, n*(len(mx)//n) + 1, n ) ][:-1]


#key expansion
keys = [key] #This will hold 10 + 1 keys each of 16 bytes

for i in range(11):
	k = []
	lastcolumn = []
	sk = shift(keys[-1][12:])
	for i in sk:
		lastcolumn.append(tohex(sbox[int(i[0], base = 16)*16 + int(i[1], base = 16) ]))

	for i in range(4):
		for a,b in zip(lastcolumn, keys[-1][i*4:i*4+4]):
			k.append( xor(a,b) )

	keys.append(k)



#msg related functions
def msgInHex(msg):
	'''transforms the msg into 128 bit pairs 0's are padded if the bits of string is not a multiple of 128 '''
	mx =  [tohex(ord(m)) for m in msg] 
	if len(mx)%16 != 0:
		mx += ["00"]*(16 - len(mx)%16)
	return mx


msg = input("Enter a message to encrypt: ")
mx = msgInHex(msg)

#encipher
#BYTE SUB
mmx = mx
for i in mmx:
	j = 0
	print(i)
	print(int(i[0], base = 16)*16 + int(i[1], base = 16))
	mmx[j] = tohex(sbox[int(i[0], base = 16)*16 + int(i[1], base = 16) ])
	j += 1

#SHIFT ROW
j = 0
for i in shifttable:
	mmx[j] = mmx[i]
	j += 1

#Mix column key


#Add round key
for i in range(1,11):
	j = 0
	for m,k in zip(mmx, keys[i] ):
		mmx[j] = xor(m,k)
		j += 1
	print(mmx)