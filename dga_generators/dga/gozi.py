import os
from datetime import datetime
from ctypes import c_uint

current_directory = os.path.dirname(os.path.abspath(__file__))

seeds = {
        'luther': {'div': 4, 'tld': '.com', 'nr': 12},
        'rfc4343': {'div': 3, 'tld': '.com', 'nr': 10},
        'nasa': {'div': 5, 'tld': '.com', 'nr': 12},
        'gpl': {'div': 5, 'tld': '.ru', 'nr': 10}
        }
        
        
class Rand:

    def __init__(self, seed):
        self.r = c_uint(seed) 

    def rand(self):
        self.r.value = 1664525*self.r.value + 1013904223
        return self.r.value

def get_words(wordlist):
    with open(current_directory + "/" + wordlist, 'r') as r:
        return [w.strip() for w in r if w.strip()]

def dga(date, wordlist):
    words = get_words(wordlist)
    diff = date - datetime.strptime("2015-01-01", "%Y-%m-%d")
    days_passed = (diff.days // seeds[wordlist]['div'])
    flag = 1
    seed = (flag << 16) + days_passed - 306607824
    r = Rand(seed) 

    for i in range(12):
        r.rand()
        v = r.rand()
        length = v % 12 + 12
        domain = ""
        while len(domain) < length:
            v = r.rand() % len(words)
            word = words[v] 
            l = len(word)
            if not r.rand() % 3:
                l >>= 1
            if len(domain) + l <= 24:
                domain += word[:l]
        domain += seeds[wordlist]['tld']
        yield domain

def generate_domains(nr_domains):
    ret = []
    while len(ret) < nr_domains:
        for wordlist in seeds.keys():
            d = datetime.now()
            for domain in dga(d, wordlist):
                ret.append(domain)
    # print(len(ret))
    return ret

if __name__ == "__main__":
    print(generate_domains(50))

