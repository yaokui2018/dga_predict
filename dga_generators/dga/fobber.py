import argparse


def ror32(v, n):
    return ((v >> n) | (v << (32 - n))) & 0xFFFFFFFF


def next_domain(r, c, l, tld):
    domain = ""
    for _ in range(l):
        r = ror32((321167 * r + c) & 0xFFFFFFFF, 16);
        domain += chr((r & 0x17FF) % 26 + ord('a'))

    domain += tld
    # print(domain)
    return domain


def dga(version):
    if version == 1:
        r = 0xC87C8A78
        c = -1719405398
        l = 17
        tld = '.net'
        # nr = 300
    elif version == 2:
        r = 0x851A3E59
        c = -1916503263
        l = 10
        tld = '.com'
        # nr = 300
    # for _ in range(nr):
    r = next_domain(r, c, l, tld)
    return r


def generate_domains(nr_domains):
    ret = []
    while len(ret) < nr_domains:
        for d in [1, 2]:
            ret.append(dga(d))
            # print(domain)
    # print(len(ret))
    return ret


if __name__ == "__main__":
    print(generate_domains(13))
