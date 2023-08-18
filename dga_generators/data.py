# -*- coding: utf-8 -*-
"""
生成DGA数据
"""
import csv
from datetime import datetime
import random
import numpy as np
from tldextract import tldextract
from tqdm import tqdm

from dga import banjori, corebot, cryptolocker, \
    dircrypt, kraken, lockyv2, pykspa, qakbot, ramdo, ramnit, simda, charbot, \
    chinad, dmsniff, dnschanger, fobber, gozi, lockyv3, murofetv1, murofetv2, murofetv3, necurs, \
    newgoz, nymaim, nymaim2, padcrypt, proslikefan, qadars, shiotob, sisron, \
    suppobox, symmi, tempedreve, tinba, unknown_malware, unnamed_javascript_dga, vawtrak

OLD_ALGORITHMS = [chinad, dmsniff, dnschanger,
                  fobber, gozi, lockyv3, murofetv1, murofetv2, murofetv3, necurs,
                  newgoz, nymaim, nymaim2, padcrypt, proslikefan, qadars, shiotob, sisron,
                  suppobox, symmi, tempedreve, tinba, unknown_malware, unnamed_javascript_dga, vawtrak]

# Location of Alexa 1M
ALEXA_1M = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'


def get_alexa(filepath='data/tranco1M.csv'):
    """读取正常域名"""
    domains = set()
    TLDs = set()
    print("读取正常域名..")
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            # if i >= num:
            #     break
            # domain = tldextract.extract(row[1]).domain
            TLDs.add(tldextract.extract(row[1]).suffix)
            domain = row[1]
            domains.add(domain)
    print("合法域名后缀：", len(TLDs))
    return list(domains), list(TLDs)


def gen_malicious(total_num_dga, TLDs):
    """Generates num_per_dga of each DGA"""
    num_per_dga = total_num_dga // (12 + 1)
    # TLDs = 'com, at, uk, pl, be, biz, co, jp, cz, de, eu, fr, info, it, ru, lv, me, name, net, nz, org, us'.split(', ')

    domains = []
    labels = []

    print("正在生成 banjori...")
    # We use some arbitrary seeds to create domains with banjori
    banjori_seeds = ['somestring', 'firetruck', 'bulldozer', 'airplane', 'racecar',
                     'apartment', 'laptop', 'laptopcomp', 'malwareisbad', 'crazytrain',
                     'thepolice', 'fivemonkeys', 'hockey', 'football', 'baseball',
                     'basketball', 'trackandfield', 'fieldhockey', 'softball', 'redferrari',
                     'blackcheverolet', 'yellowelcamino', 'blueporsche', 'redfordf150',
                     'purplebmw330i', 'subarulegacy', 'hondacivic', 'toyotaprius',
                     'sidewalk', 'pavement', 'stopsign', 'trafficlight', 'turnlane',
                     'passinglane', 'trafficjam', 'airport', 'runway', 'baggageclaim',
                     'passengerjet', 'delta1008', 'american765', 'united8765', 'southwest3456',
                     'albuquerque', 'sanfrancisco', 'sandiego', 'losangeles', 'newyork',
                     'atlanta', 'portland', 'seattle', 'washingtondc']

    segs_size = max(1, num_per_dga // len(banjori_seeds))
    for banjori_seed in banjori_seeds:
        domains += banjori.generate_domains(segs_size, banjori_seed)
        labels += ['banjori'] * segs_size

    print("正在生成 corebot...")
    domains += corebot.generate_domains(num_per_dga)
    labels += ['corebot'] * num_per_dga

    print("正在生成 cryptolocker...")
    # Create different length domains using cryptolocker
    crypto_lengths = range(8, 32)
    segs_size = max(1, num_per_dga // len(crypto_lengths))
    for crypto_length in crypto_lengths:
        domains += cryptolocker.generate_domains(segs_size,
                                                 seed_num=random.randint(1, 1000000),
                                                 length=crypto_length)
        labels += ['cryptolocker'] * segs_size

    print("正在生成 dircrypt...")
    domains += dircrypt.generate_domains(num_per_dga)
    labels += ['dircrypt'] * num_per_dga

    # generate kraken and divide between configs
    print("正在生成 kraken...")
    kraken_to_gen = max(1, num_per_dga // 2)
    domains += kraken.generate_domains(kraken_to_gen, datetime(2016, 1, 1), 'a', 3)
    labels += ['kraken'] * kraken_to_gen
    domains += kraken.generate_domains(kraken_to_gen, datetime(2016, 1, 1), 'b', 3)
    labels += ['kraken'] * kraken_to_gen

    # generate locky and divide between configs
    print("正在生成 locky...")
    locky_gen = max(1, num_per_dga // 11)
    for i in range(1, 12):
        domains += lockyv2.generate_domains(locky_gen, config=i)
        labels += ['locky'] * locky_gen

    # Generate pyskpa domains
    print("正在生成 pykspa...")
    domains += pykspa.generate_domains(num_per_dga, datetime(2016, 1, 1))
    labels += ['pykspa'] * num_per_dga

    # Generate qakbot
    print("正在生成 qakbot...")
    domains += qakbot.generate_domains(num_per_dga, tlds=[])
    labels += ['qakbot'] * num_per_dga

    # ramdo divided over different lengths
    print("正在生成 ramdo...")
    ramdo_lengths = range(8, 32)
    segs_size = max(1, num_per_dga // len(ramdo_lengths))
    for rammdo_length in ramdo_lengths:
        domains += ramdo.generate_domains(segs_size,
                                          seed_num=random.randint(1, 1000000),
                                          length=rammdo_length)
        labels += ['ramdo'] * segs_size

    # ramnit
    print("正在生成 ramnit...")
    domains += ramnit.generate_domains(num_per_dga, 0x123abc12)
    labels += ['ramnit'] * num_per_dga

    # simda
    print("正在生成 simda...")
    simda_lengths = range(8, 32)
    segs_size = max(1, num_per_dga // len(simda_lengths))
    for simda_length in range(len(simda_lengths)):
        domains += simda.generate_domains(segs_size,
                                          length=simda_length,
                                          tld=None,
                                          base=random.randint(2, 2 ** 32))
        labels += ['simda'] * segs_size

    dgas = []
    # 添加TLD
    for domain in domains:
        tdlidx = np.random.randint(len(TLDs))
        domain += "." + TLDs[tdlidx]
        dgas.append(domain)

    # ==================================
    # 老算法，生成. 每个算法生成数量是 num_per_dga / 2
    # ==================================
    print("正在生成 OLD_ALGORITHMS...")
    for algorithm in OLD_ALGORITHMS:
        dgas += algorithm.generate_domains(num_per_dga // 2)
        labels += ['olddga'] * (num_per_dga // 2)

    # 生成数量是 num_per_dga * 2
    print("正在生成 charbot...")
    dgas += charbot.generate_domains(num_per_dga * 2)
    labels += ['charbot'] * num_per_dga * 2

    return dgas, labels


def gen_data(save_path, dga_radio=1.2):
    """
    生成数据
    :param save_path: 数据保存路径
    :param dga_radio: DGA占比正常域名的比例
    :return:
    """
    domains, TLDs = get_alexa()
    labels = ['benign'] * len(domains)
    print("正常域名：", len(domains))

    dga_domains, dga_labels = gen_malicious(int(len(domains) * dga_radio), TLDs)
    print("dga域名：", len(dga_domains))
    domains += dga_domains
    labels += dga_labels

    print("总域名数：", len(domains))

    data = zip(domains, labels)
    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)  # 写入数据

    print("数据保存成功：", save_path)


if __name__ == '__main__':
    save_path = 'save_data.csv'
    gen_data(save_path)
