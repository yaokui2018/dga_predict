import hashlib
from datetime import datetime, timedelta
import argparse


def generate_domains(nr=1020):
    ret = []
    date = datetime.now()
    for index in range(nr):
        seed = 7*[0]
        seed[0] = ((date.year & 0xFF) + 0x30) & 0xFF
        seed[1] = date.month 
        seed[2] = (date.day//7)*7
        r = index
        for i in range(4):
            seed[3+i] = r & 0xFF
            r >>= 8

        seed_str = ""
        for i in range(7):
            seed_str += chr((seed[i]))

        m = hashlib.md5()
        m.update(seed_str.encode('latin1'))
        md5 = m.digest()

        domain = ""
        for m in md5:
            d = (m & 0x1F) + ord('a')
            c = (m >> 3) + ord('a')
            if d != c:
                if d <= ord('z'):
                    domain += chr(d)
                if c <= ord('z'):
                    domain += chr(c)

        tlds = [".ru", ".biz", ".info", ".org", ".net", ".com"]
        for i, tld in enumerate(tlds): 
            m = len(tlds) - i
            if not index % m: 
                domain += tld
                break
        ret.append(domain)

    return ret


if __name__=="__main__":

    print(generate_domains(100))
