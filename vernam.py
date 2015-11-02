from random import *
msg = "Mass bunk today"



def encipher():
	msg = input("\n\nGimme something to encrypt: ")
	key = keygen(msg)

	ct = "".join([ chr(ord('a') + (ord(msg[i].lower()) + key[i] - ord('a') )%26) if msg[i].isalpha() else msg[i] for i in range(len(msg))])

	print( "\n=======Encrypting the data========")
	print( key )
	print("Msg: " + msg + "\n" + "Secret Text: " + ct)
	return ct,key

def decipher(ct, key):
	pt = "".join([chr( ord('a') + (ord(ct[i]) - key[i] - ord('a') )%26) if ct[i].isalpha() else ct[i] for i in range(len(ct))])
	
	print("\n========Decrypting the data=========")
	print("Secret Text: " + ct + "\n" + "Message: " + pt)


def keygen(msg):
	return [ randint(0, 100) for i in range(len(msg)) ] 

if __name__ == '__main__':
	(ct, key) = encipher()
	decipher(ct, key)