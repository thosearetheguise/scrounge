from math import log2

def get_entropy(password):
    alphabet = ''.join(set(password))
    print(alphabet)
    length = len(password)
    ent = log2(len(alphabet*length))
    print(ent)

password = "aaaaaaaaaa"

good_password = "+!}*RWq3CbQkT-CpE"

get_entropy(password)

get_entropy(good_password)


