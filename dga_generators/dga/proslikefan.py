import argparse
from ctypes import c_int
from datetime import datetime

def dga(date, magic='prospect'):
    tlds = ["eu", "biz", "se", "info", "com", "net", "org", "ru", "in",
           "name"]
    for i in range(1):
        for tld in tlds:
            seed_string = '.'.join([str(s) for s in 
                    [magic, date.month, date.day, date.year, tld]])
            r = abs(hash_string(seed_string)) + i
            domain = ""
            k = 0
            while(k < r % 7 + 6):
                r = abs(hash_string(domain + str(r))) 
                domain += chr(r % 26 + ord('a')) 
                k += 1
            domain += '.' + tld
            yield domain


def hash_string(s):
    h = c_int(0) 
    for c in s:
        h.value = (h.value << 5) - h.value + ord(c)
    return h.value

def generate_domains(nr_domains):
    ret = []
    while len(ret) < nr_domains:
        for magic in ['prospect', 'OK']:
            d = datetime.now()
            for domain in dga(d, magic):
                ret.append(domain)
                # print(domain)
    print(len(ret))
    return ret

if __name__=="__main__":
    """ known magic seeds are "prospect" and "OK" """

    print(generate_domains(20))
