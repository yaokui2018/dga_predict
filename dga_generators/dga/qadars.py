import argparse
import time
from datetime import datetime
import time
import string

def rand(r, seed):
    return  (seed - 1043968403*r) & 0x7FFFFFFF

def dga(date, seed):
    charset = string.ascii_lowercase + string.digits
    if seed in [0xE1F2, 0xE1F1, 0xE1F5]:
        tlds = [".com", ".org", ".net"]
    else:
        tlds = [".net", ".org", ".top"]
    unix = int(time.mktime(date.timetuple()))
    b = 7*24*3600
    c = 4*24*3600
    r = unix - (unix-c) % b
    for i in range(1):
        domain = ""
        for _ in range(12):
            r = rand(r, seed)
            domain += charset[r % len(charset)]
        r = rand(r, seed)
        tld = tlds[r % 3]
        domain += tld
        yield domain

def generate_domains(nr_domains):
    ret = []
    seeds = ["89f5", "4449", "E1F1", "E1F2", "E08A", "E1F5"]
    while len(ret) < nr_domains:
        d = datetime.now()
        for seed in seeds:
            for domain in dga(d, int(seed, 16)):
                ret.append(domain)
                # print(domain)
    print(len(ret))
    return ret

if __name__ == "__main__":

    print(generate_domains(19))