'''
	Implements caesar cipher 
	Usage: encipher() -> for encrypting a message
		   decryptor() -> for decrypting a message
'''

print("Et, Tu Brute????? Nruqjrjsyx hfjxfw hnumjw Fzymtw- Mnrfsxmz Xfnsn\n")




def encipher():

	plainText = input("\n\nGimme something to encrypt: ")

	key = int(input("Give me a key too: ")) 

	cipheredText = []

	for p in plainText:

		if p.isupper():
			c = chr( ord('A') + (ord(p) + key - ord('A'))%26 ) 
		elif p.islower():
			c = chr( ord('a') + (ord(p) + key - ord('a'))%26 ) 
		else:
			c = p

		cipheredText.append(c)



	cipheredText = ''.join(cipheredText)

	print("\n"+ "#"*30, "\nYour ciphered Text is", cipheredText , "\n" + "#"*30)







def decryptor():

	cipheredText = input("\n\nGimme something to decrypt: ")

	key = int(input("Give me a key too: ")) 

	plainText = []

	for p in cipheredText:

		if p.isupper():
			c = chr( ord('A') + (ord(p) -  key - ord('A'))%26 ) 
		elif p.islower():
			c = chr( ord('a') + (ord(p) - key - ord('a'))%26 ) 
		else:
			c = p

		plainText.append(c)



	plainText = ''.join(plainText)

	print("\n"+ "#"*30, "\nYour plain text is", plainText, "\n" + "#"*30)




if __name__ == '__main__':
	encipher()
	decryptor()