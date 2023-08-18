import argparse

def get_next_domain(domain):
    qwerty = 'qwertyuiopasdfghjklzxcvbnm123945678'

    def sum_of_characters(domain):
        return sum([ord(d) for d in domain[:-3]])

    sof = sum_of_characters(domain)
    ascii_codes = [ord(d) for d in domain] + 100*[0]
    old_hostname_length = len(domain) - 4
    for i in range(0, 66):
        for j in range(0, 66):
            edi = j + i
            if edi < 65:
                p = (old_hostname_length * ascii_codes[j]) 
                cl = p ^ ascii_codes[edi] ^ sof
                ascii_codes[edi] = cl & 0xFF

    """
        calculate the new hostname length
        max: 255/16 = 15
        min: 10
    """
    cx = ((ascii_codes[2]*old_hostname_length) ^ ascii_codes[0]) & 0xFF
    hostname_length = int(cx/16) # at most 15
    if hostname_length < 10:
        hostname_length = old_hostname_length

    """
        generate hostname
    """
    for i in range(hostname_length):
        index = int(ascii_codes[i]/8) # max 31 --> last 3 chars of qwerty unreachable
        bl = ord(qwerty[index])
        ascii_codes[i] = bl

    hostname = ''.join([chr(a) for a in ascii_codes[:hostname_length]])

    """
        append .net or .com (alternating)
    """
    tld = '.com' if domain.endswith('.net') else '.net'
    domain = hostname + tld

    return domain

def generate_domains(nr_domains):
    ret = []
    domain = "4ypv1eehphg3a.com"
    for i in range(nr_domains):
        domain = get_next_domain(domain)
        ret.append(domain)
    # print(len(ret))
    return ret

if __name__=="__main__":
    """ example seed domain: 4ypv1eehphg3a.com """


    print(generate_domains(10))

