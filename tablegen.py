class BinPol:

    def __init__(self, x, irreducible_polynomial=None, grade=None):
        self.dec = x
        self.hex = hex(self.dec)[2:]
        self.bin = reversed(list(bin(self.dec)[2:]))
        self.bin = [int(bit) for bit in self.bin]

        if grade is not None:
            self.grade = grade
        else:
            self.grade = len(self.bin)-1

        self.irreducible_polynomial = irreducible_polynomial

    def __str__(self):
        h = self.hex
        if self.dec < 16:
            h = '0' + h
        return h

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.grade

    def __setitem__(self, key, value):
        if value in [0, 1]:
            while len(self.bin) <= key:
                self.bin.append(0)

            self.bin[key] = value

        self.__update_from_bin()

    def __getitem__(self, key):
        if key < len(self.bin):
            return self.bin[key]
        else:
            return 0

    def __add__(self, x):
        r = BinPol(self.dec, self.irreducible_polynomial)

        for i, a in enumerate(x.bin):
            r[i] = r[i] ^ a

        r.__update_from_bin()
        return r

    def __mul__(self, x):
        r = BinPol(0, self.irreducible_polynomial)
        for i, a in enumerate(self.bin):
            for j, b in enumerate(x.bin):
                if a and b:
                    r[i+j] = r[i+j] ^ 1

        r.__update_from_bin()
        return r

    def __pow__(self, x):
        r = BinPol(1, self.irreducible_polynomial)

        for i in range(1, x+1):
            r = r * BinPol(self.dec)
            r.__update_from_bin()

            if (r.irreducible_polynomial
                    and r.grade >= r.irreducible_polynomial.grade):
                r = r + r.irreducible_polynomial
                r.__update_from_bin()

        return r

    def __update_from_bin(self):

        self.__remove_most_significant_zeros()

        self.dec = 0
        for i, a in enumerate(self.bin):
            if a:
                self.dec += 2**i

        self.hex = hex(self.dec)[2:]

        self.grade = len(self.bin)-1

    def __remove_most_significant_zeros(self):
        last = 0
        for i, a in enumerate(self.bin):
            if a:
                last = i
        del(self.bin[last+1:])


def inv_pol(pol, antilog, log):
    if pol.dec == 0:
        return BinPol(0, pol.irreducible_polynomial)
    else:
        return BinPol(antilog[0xFF - log[pol.dec].dec].dec,
                      pol.irreducible_polynomial)


def affine_transformation(b):
    b1 = BinPol(b.dec, b.irreducible_polynomial)
    c = BinPol(0b01100011)

    for i in range(8):
        b1[i] = b[i] ^ b[(i+4) % 8]
        b1[i] ^= b[(i+5) % 8]
        b1[i] ^= b[(i+6) % 8]
        b1[i] ^= b[(i+7) % 8]
        b1[i] ^= c[i]

    return b1


def generate():
    irreducible_polynomial = BinPol(0b100011011)
    
    primitive = BinPol(3, irreducible_polynomial)

    antilog = [primitive**i for i in range(256)]
    
    log = [BinPol(0, irreducible_polynomial)
           for i in range(256)]
    for i, a in enumerate(antilog):
        log[a.dec] = BinPol(i, irreducible_polynomial)
   

    inv = [inv_pol(BinPol(i), antilog, log) for i in range(256)]
   
    sbox = [affine_transformation(a) for a in inv]
    #print(sbox)
   

    isbox = [BinPol(0, irreducible_polynomial)
             for i in range(256)]
    for i, a in enumerate(sbox):
        isbox[a.dec] = BinPol(i, irreducible_polynomial)
    #print(isbox)

    return (sbox , isbox)


