from datetime import datetime, timedelta
import base64
import argparse


def dga(d, day_index, tld_index):
    tlds = [x.encode('ascii') for x in [".com", ".org", ".net", ".info"]]
    d -= timedelta(days=day_index)
    ds = d.strftime("%d%m%Y").encode('latin1')
    domain = base64.b64encode(ds).lower().replace(b"=", b"a") + tlds[tld_index % len(tlds)]
    return domain.decode('latin1')


def generate_domains(nr_domains):
    ret = []
    d = datetime.now()
    for i in range(nr_domains):
        domain = dga(d, i % 10, i // 10)
        ret.append(domain)
    # print(len(ret))
    return ret


if __name__ == "__main__":
    print(generate_domains(100))
