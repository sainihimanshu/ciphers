from random import *
msg = "Mass bunk today"
def encipher():
	#if (len(msg) == 0):
	msg = input("\n\nGimme something to encrypt: ")

	key = keygen(msg)
	ct = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(msg, key)])
	print( "\n"*5+"#"*10 + "\tEncrypting\t"+ "#"*10)
	print("Msg: " + msg + "\n" + "Key: " + key + "\n" + "Secret Text: " + ct)
	return ct,key

def decipher(ct, key):
	pt = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(ct, key)])
	print("\n"*5+ "#"*10 + "\tDecrypting\t"+ "#"*10)

	print("Secret Text: " + ct + "\n" + "Message:" + pt)


def keygen(msg):
	return "".join([ chr(randint(ord('a'), ord('z'))) for i in range(len(msg)) ]) 

if __name__ == '__main__':
	(ct, key) = encipher()
	decipher(ct, key)