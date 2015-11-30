from random import *


def sub_bytes(state, inv=False):

    if inv == False: 
        box = sbox
    else: 
        box = sboxi

    for i in range(len(state)):
        for j in range(len(state[i])):
            row = state[i][j] // 0x10
            col = state[i][j] % 0x10
            box_elem = box[16 * row + col]
            state[i][j] = box_elem

    return state


def shift_rows(state, inv=False):
    count = 1

    if inv == False: 
        for i in range(1, nb):
            state[i] = left_shift(state[i], count)
            count += 1
    else:  
        for i in range(1, nb):
            state[i] = right_shift(state[i], count)
            count += 1

    return state


def mix_columns(state, inv=False):
    
    for i in range(nb):

        if inv == False:  
            s0 = mul_by_02(state[0][i]) ^ mul_by_03(state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ mul_by_02(state[1][i]) ^ mul_by_03(state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ mul_by_02(state[2][i]) ^ mul_by_03(state[3][i])
            s3 = mul_by_03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ mul_by_02(state[3][i])
        else:  
            s0 = mul_by_0e(state[0][i]) ^ mul_by_0b(state[1][i]) ^ mul_by_0d(state[2][i]) ^ mul_by_09(state[3][i])
            s1 = mul_by_09(state[0][i]) ^ mul_by_0e(state[1][i]) ^ mul_by_0b(state[2][i]) ^ mul_by_0d(state[3][i])
            s2 = mul_by_0d(state[0][i]) ^ mul_by_09(state[1][i]) ^ mul_by_0e(state[2][i]) ^ mul_by_0b(state[3][i])
            s3 = mul_by_0b(state[0][i]) ^ mul_by_0d(state[1][i]) ^ mul_by_09(state[2][i]) ^ mul_by_0e(state[3][i])

        state[0][i] = s0
        state[1][i] = s1
        state[2][i] = s2
        state[3][i] = s3

    return state

from aestables import *

def key_expansion(key):

    key_symbols = [ord(symbol) for symbol in key]

    key_schedule = [[] for i in range(4)]
    for r in range(4):
        for c in range(nk):
            key_schedule[r].append(key_symbols[r + 4 * c])

    for col in range(nk, nb * (nr + 1)): 
        if col % nk == 0:
            tmp = [key_schedule[row][col - 1] for row in range(1, 4)]
            tmp.append(key_schedule[0][col - 1])

            for j in range(len(tmp)):
                sbox_row = tmp[j] // 0x10
                sbox_col = tmp[j] % 0x10
                sbox_elem = sbox[16 * sbox_row + sbox_col]
                tmp[j] = sbox_elem

            for row in range(4):
                s = (key_schedule[row][col - 4]) ^ (tmp[row]) ^ (rcon[row][int(col / nk - 1)])
                key_schedule[row].append(s)
        else:
            for row in range(4):
                s = key_schedule[row][col - 4] ^ key_schedule[row][col - 1]
                key_schedule[row].append(s)

    return key_schedule


def add_round_key(state, key_schedule, round=0):

    for col in range(nk):
        s0 = state[0][col] ^ key_schedule[0][nb * round + col]
        s1 = state[1][col] ^ key_schedule[1][nb * round + col]
        s2 = state[2][col] ^ key_schedule[2][nb * round + col]
        s3 = state[3][col] ^ key_schedule[3][nb * round + col]

        state[0][col] = s0
        state[1][col] = s1
        state[2][col] = s2
        state[3][col] = s3

    return state


# Small helpful functions block

def left_shift(array, count):
    """Rotate the array over count times"""
    return array[count:] + array[:count]


def right_shift(array, count):
    """Rotate the array over count times"""
    return array[len(array) - count:] + array[:len(array) - count]



def encrypt(msg, key):
    #key - str; msg - str

    msg = [ord(m) for m in msg]

    # breaking data in 4x4 block
    state = [[] for j in range(4)]
    for r in range(4):
        for c in range(nb):
            state[r].append(msg[r + 4 * c])

    key_schedule = key_expansion(key)

    state = add_round_key(state, key_schedule)

    for rnd in range(1, nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key_schedule, rnd)

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, rnd + 1)

    et = [0 for i in range(4 * nb)]

    for r in range(4):
        for c in range(nb):
            et[r + 4 * c] = state[r][c]

    return "".join([chr(e) for e in et])


def decrypt(cipher, key):

    cipher = [ord(m) for m in cipher]

    state = [[] for i in range(nb)]
    for r in range(4):
        for c in range(nb):
            state[r].append(cipher[r + 4 * c])

    key_schedule = key_expansion(key)

    state = add_round_key(state, key_schedule, nr)

    rnd = nr - 1
    while rnd >= 1:
        state = shift_rows(state, inv=True)
        state = sub_bytes(state, inv=True)
        state = add_round_key(state, key_schedule, rnd)
        state = mix_columns(state, inv=True)

        rnd -= 1

    state = shift_rows(state, inv=True)
    state = sub_bytes(state, inv=True)
    state = add_round_key(state, key_schedule, rnd)

    pt = [None for i in range(4 * nb)]
    for r in range(4):
        for c in range(nb):
            pt[r + 4 * c] = state[r][c]

    return "".join([chr(p) for p in pt])


if __name__ == '__main__':
        
    msg = input("Enter a message to encrypt: ")
    lm = len(msg)

    #msg padding with 0
    if len(msg)%16 != 0:
        msg += "z"*(16 - len(msg)%16)

    key = [ chr(choice(range(ord("A"), ord("Z") ))) for i in range(16) ] #16 random alphabets for key
    keyStr = "".join(key) #key in str format
    keyNum = [ord(i) for i in key] 

    et = encrypt(msg, key)
    print("Encrypted Text: {0}\n".format(et))

    pt = decrypt(et, key)
    print("Decrypted Text: {0}\n".format(pt[0:lm]))
