#generating key
from random import *

keys = [chr(choice(range(ord("A"), ord("Z") ))) for i in range(16) ] #16 random alphabets

shift = lambda i: i[1:] + [i[0]] #left circular shift