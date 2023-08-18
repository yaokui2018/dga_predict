from datetime import datetime
import argparse
from ctypes import c_int


def prng(seed_string):
    result = c_int()
    for c in seed_string:
        a = result.value
        result.value = (result.value << 5)
        tmp = result.value - a
        result.value = tmp + ord(c)
        result.value &= result.value

    return result.value


def generate_domains(nr_domains):
    seed = "OK"
    tlds = ["cc", "co", "eu"]
    dga_domains = []
    for i in range(nr_domains):
        d = datetime.now()
        for j, tld in enumerate(tlds):
            ss = ".".join([str(s) for s in [seed, d.month, d.day, d.year, tld]])
            r = abs(prng(ss)) + i
            domain = ""
            k = 0
            while k < (r % 7 + 6):
                r = abs(prng(domain + str(r)))
                domain += chr(r % 26 + ord('a'))
                k += 1
            dga_domains.append("{}.{}".format(domain, tld))
    return dga_domains


if __name__ == "__main__":
    print(generate_domains(110))
