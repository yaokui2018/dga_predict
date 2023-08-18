import json
import argparse
import os
from datetime import datetime
import hashlib


current_directory = os.path.dirname(os.path.abspath(__file__))
class Rand:

    def __init__(self, seed, year, yday, offset=0):
        m = self.md5(seed)
        s = "{}{}{}".format(m, year, yday + offset)
        self.hashstring = self.md5(s)

    @staticmethod
    def md5(s):
        return hashlib.md5(s.encode('ascii')).hexdigest()

    def getval(self):
        v = int(self.hashstring[:8], 16)
        self.hashstring = self.md5(self.hashstring[7:])
        return v

def dga(date):
    with open(current_directory + "/words.json", "r") as r:
        wt = json.load(r)

    seed = "3138C81ED54AD5F8E905555A6623C9C9"
    daydelta = 10
    maxdomainsfortry = 64
    year = date.year % 100
    yday = date.timetuple().tm_yday - 1

    for dayoffset in range(daydelta + 1):
        r = Rand(seed, year, yday - dayoffset)
        for _ in range(maxdomainsfortry):
            domain = ""
            for s in ['firstword', 'separator', 'secondword', 'tld']:
                ss = wt[s]
                domain += ss[r.getval() % len(ss)]
            yield domain

def generate_domains(nr_domains):
    ret = []
    while len(ret) < nr_domains:
        date = datetime.now()
        for domain in dga(date):
            ret.append(domain)
    # print(len(ret))
    return ret

if __name__=="__main__":

    print(generate_domains(1000))
