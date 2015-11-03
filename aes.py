#generating key
from random import *
from aestables import *

tohex = lambda num: "{:02x}".format(num) #converts an int to a hex 
toint = lambda x: int(str(x) , base = 16) #converts an hex to an int
 
key = [tohex(choice(range(ord("A"), ord("Z") ))) for i in range(16) ] #16 random alphabets

shift = lambda i: i[1:] + [i[0]] #left circular shift

xor = lambda x1, x2: tohex(toint(x1) ^ toint(x2) )

slice = lambda mx, n:  [ mx[i:i+n] for i in range(0, n*(len(mx)//n) + 1, n ) ][:-1]

hex2value = lambda s, table: table[int(s[0], base = 16)*16 + int(s[1], base = 16) ]

hex2string = lambda hexTable: "".join(chr(toint(i)) for i in hexTable)


#key expansion
keys = [key] #This will hold 10 + 1 keys each of 16 bytes

for i in range(11):
	k = []
	lastcolumn = []
	sk = shift(keys[-1][12:])
	for i in sk:
		lastcolumn.append(tohex(hex2value(i, sbox)))

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


mmx = mx.copy()


#encipher
#BYTE SUB
def byteSub():
	j = 0
	for i in mmx:
		mmx[j] = tohex(hex2value(i, sbox))
		j += 1

#SHIFT ROW
def rowShift():
	j = 0
	for i in shifttable:
		mmx[j] = mmx[i]
		j += 1

#Mix column key
def mixColumn():
	j = 0
	for oo in range(4):
		for o in range(4):
			for k in range(4):
				l = str(mmx[k+oo*4])
				i = str(mmx[k*4 + o])
				#print(l,i) 
				if k == 0: t1 = tohex(hex2value( str(tohex((hex2value(l, L) + hex2value(i, L))%0xff)) , E))
				if k != 0: 
					t = xor(t1, tohex(hex2value(str( tohex((hex2value(l, L) + hex2value(i, L))%0xff)) , E)))
					t1 = t
				#print(l, i, t1)
			mmx[j] = t 
			j += 1


#Add round key
#xors the 16 bytes of key with 16 byte current state of message 
def roundKey(i):
	j = 0
	for m,k in zip( mmx, keys[i] ):
		mmx[j] = xor(m,k)
		j += 1
	print(mmx)

def encrypt():
	roundKey(0) #iteration 0

	for i in range(1,8):
		byteSub()
		rowShift()
		mixColumn()
		roundKey(i)

	byteSub()
	rowShift()
	roundKey(i)

	roundKey(9)

encrypt()
hex2string(key)
hex2string(mmx)
