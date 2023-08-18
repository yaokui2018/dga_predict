from ctypes import c_uint
import argparse

class Rand():

    def __init__(self, seed):
        self.r = c_uint(seed)
        self.m = 1103515245
        self.a = 12345

    def rand(self):
        self.r.value = self.r.value*self.m + self.a
        self.r.value &= 0x7FFFFFFF
        return self.r.value


def dga(r):
    length = r.rand()%5 + 7
    domain = ""
    for i in range(length):
        domain += chr(r.rand() % 26 + ord('a'))
    domain += ".top"
    yield domain


def generate_domains(nr_domains):
    ret = []
    seed = "DEADBEEF"
    r = Rand(int(seed, 16))
    for nr in range(nr_domains):
        for domain in dga(r):
            ret.append(domain)
    print(len(ret))
    return ret

if __name__=="__main__":

    print(generate_domains(10))

