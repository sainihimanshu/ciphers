import math
msg = "Mass bunk today"

def encipher():
	msg = input("\n\nGimme something to encrypt: ")
	cols = int(input("Enter the number of columns: "))

	print( "\n=======Encrypting the data========")
	m = msg.replace(' ' , '')

	sl = []
	secret = ""
	rows = math.ceil(len(m)/cols)
	for i in range(rows):
		start = cols*i 
		tempm = m[start:start+cols]
		if len(tempm) != cols:
			tempm += 'q'*(cols - len(tempm))
		sl.append(tempm)

	for i in range(cols):
		for sls in sl:
			secret += sls[i]
		secret += " "
		
	#print(sl)
	#print(secret)
	ct = secret

	print("Msg: " + msg + "\n" + "Secret Text: " + ct)
	return ct,cols

def decipher(ct, cols):
	print("\n========Decrypting the data=========")
	finalMsg = ""
	dl = ct.split(' ')[:-1]
	for i in range(len(dl[0])):
		for dls in dl:
			finalMsg += dls[i]

	print(finalMsg)
	print("Secret Text: " + ct + "\n" + "Message: " + finalMsg)



if __name__ == '__main__':
	(ct, cols) = encipher()
	decipher(ct, cols)