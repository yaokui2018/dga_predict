import hashlib
import random
from datetime import datetime, timedelta
import argparse


def generate_domains(nr_domains):
    ret = []
    key = int(str(random.randint(0, 10000)), 16)
    date = datetime.now()
    for index in range(nr_domains):
        seed = 8*[0]
        seed[0] = ((date.year & 0xFF) + 0x30) & 0xFF
        seed[1] = date.month & 0xFF
        seed[2] = date.day & 0xFF
        seed[3] = 0
        r = (index) & 0xFFFFFFFE
        for i in range(4):
            seed[4+i] = r & 0xFF
            r >>= 8

        seed_str = ""
        for i in range(8):
            k = (key >> (8*(i%4))) & 0xFF if key else 0
            seed_str += chr((seed[i] ^ k))

        m = hashlib.md5()
        m.update(seed_str.encode('latin1'))
        md5 = m.digest()

        domain = ""
        for m in md5:
            tmp = (m & 0xF) + (m >> 4) + ord('a')
            if tmp <= ord('z'):
                domain += chr(tmp)

        tlds = [".biz", ".info", ".org", ".net", ".com"]
        for i, tld in enumerate(tlds): 
            m = len(tlds) - i
            if not index % m: 
                domain += tld
                break
        ret.append(domain)

    return ret

if __name__=="__main__":
    # known keys:
    # -k D6D7A4BE
    # -k DEADC2DE
    # -k D6D7A4B1
    print(generate_domains(100))
