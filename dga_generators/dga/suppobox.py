"""
    generate domains according to: 
    - https://www.endgame.com/blog/malware-with-a-personal-touch.html
    - http://www.rsaconference.com/writable/presentations/file_upload/br-r01-end-to-end-analysis-of-a-domain-generating-algorithm-malware-family.pdf 

    requires words1.txt, words2.txt and words3.txt

    Thanks to Sándor Nemes who provided the third wordlist. It is taken
    from this sample:
    https://www.virustotal.com/en/file/4ee8484b95d924fe032feb8f26a44796f37fb45eca3593ab533a06785c6da8f8/analysis/
"""
import os
import time
from datetime import datetime
import argparse

current_directory = os.path.dirname(os.path.abspath(__file__))
def generate_domains_(time_, word_list):
    with open(current_directory + "/words{}.txt".format(word_list), "r") as r:
        words = [w.strip() for w in r.readlines()]

    if not time_:
        time_ = time.time()
    seed = int(time_) >> 9
    for c in range(85):
        nr = seed
        res = 16 * [0]
        shuffle = [3, 9, 13, 6, 2, 4, 11, 7, 14, 1, 10, 5, 8, 12, 0]
        for i in range(15):
            res[shuffle[i]] = nr % 2
            nr = nr >> 1

        first_word_index = 0
        for i in range(7):
            first_word_index <<= 1
            first_word_index ^= res[i]

        second_word_index = 0
        for i in range(7, 15):
            second_word_index <<= 1
            second_word_index ^= res[i]
        second_word_index += 0x80

        first_word = words[first_word_index]
        second_word = words[second_word_index]
        tld = ".net"
        yield "{}{}{}".format(first_word, second_word, tld)
        seed += 1

def generate_domains(nr_domains):
    ret = []
    datefmt = "%Y-%m-%d %H:%M:%S"
    while len(ret) < nr_domains:
        for set in [1, 2, 3]:
            time_str = datetime.now().strftime(datefmt)
            time_ = time.mktime(datetime.strptime(time_str, datefmt).timetuple())
            for domain in generate_domains_(time_, set):
                ret.append(domain)
    # print(len(ret))
    return ret

if __name__ == "__main__":

    print(generate_domains(1000))