import hashlib
from datetime import datetime, timedelta
import struct
import argparse

def get_seed(seq_nr, date):
    key = "\x01\x05\x19\x35"
    seq_nr = struct.pack('<I', seq_nr) 
    year = struct.pack('<H', date.year)
    month = struct.pack('<H', date.month)
    day = struct.pack('<H', date.day)
    m = hashlib.md5()
    m.update(seq_nr)
    m.update(year)
    m.update(key.encode('latin1'))
    m.update(month)
    m.update(key.encode('latin1'))
    m.update(day)
    m.update(key.encode('latin1'))
    return m.hexdigest()

def create_domain(seq_nr, date):
    def generate_domain_part(seed, nr):
        part = [] 
        for i in range(nr-1):
            edx = seed % 36
            seed //= 36
            if edx > 9:
                char = chr(ord('a') + (edx-10))
            else:
                char = chr(edx + ord('0'))
            part += char
            if seed == 0:
                break
        part = part[::-1]
        return ''.join(part)    

    def hex_to_int(seed):
        indices = range(0, 8, 2)
        data = [seed[x:x+2] for x in indices]
        seed = ''.join(reversed(data))
        return int(seed,16)

    seed_value = get_seed(seq_nr, date)
    domain = ""
    for i in range(0,16,4):
        seed = seed_value[i*2:i*2+8]
        seed = hex_to_int(seed)
        domain += generate_domain_part(seed, 8)
    if seq_nr % 4 == 0:
        domain += ".com"
    elif seq_nr % 3 == 0:
        domain += ".org"
    elif seq_nr % 2 == 0:
        domain += ".biz"
    else:
        domain += ".net"
    return domain

def generate_domains(nr_domains):
    ret = []
    d = datetime.today()
    for seq_nr in range(nr_domains):
        domain = create_domain(seq_nr, d)
        ret.append(domain)
                # print(domain)
    # print(len(ret))
    return ret

if __name__=="__main__":

    print(generate_domains(100))
