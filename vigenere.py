def encipher(plainText = "himanhimanhimanhima", key = "hello"):

	plainText = input("\n\nGimme something to encrypt: ")
	key = input("Give me a key(word) too: ")

	cipheredText = []
	l = len(key)
	j = 0
	for i in range(len(plainText)):
		if plainText[i].isupper():
			c = chr( ord('A') + (ord(plainText[i]) + ord(key[j%l].uppper()) - 2*ord('A'))%26 )
			j += 1 
		elif plainText[i].islower():
			c = chr( ord('a') + (ord(plainText[i]) + ord(key[j%l].lower()) - 2*ord('a'))%26  ) 
			j += 1
		else:	
			c = plainText[i]
		#print(i%l)
		cipheredText.append(c)

	cipheredText = ''.join(cipheredText)

	print("\nYour ciphered Text is", cipheredText , "\n" )
	return (cipheredText, key)


def decipher(ct, key):

	msgText = []
	l = len(key)
	j = 0
	for i in range(len(ct)):
		if ct[i].isupper():
			c = chr( ord('A') + (ord(ct[i]) - ord(key[j%l].uppper()) )%26 )
			j += 1 
		elif ct[i].islower():
			c = chr( ord('a') + (ord(ct[i]) - ord(key[j%l].lower()) )%26  ) 
			j += 1
		else:	
			c = ct[i]
		#print(i%l)
		msgText.append(c)
		#print(c)

	msgText = ''.join(msgText)

	print("\nYour plain Text is", msgText , "\n" )

if __name__ == "__main__":
	(ct, key) = encipher()
	decipher(ct, key)