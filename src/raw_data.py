# -*- coding: utf-8 -*-
"""
@author: zhangzhen
@software: PyCharm
@file: raw_data.py.py
@time: 2022/5/19 12:08
"""
import codecs
import time
import json
import collections
from tqdm import tqdm

rawdata_path = '/Users/any/data/new_top_raw_small.json'
# rawdata_path = '/Users/any/data/top_raw.json'

idx2node = {}
node2idx = {}

USE_SOURCES = [6, 202, 502, 2022, 2023, 2024, 203, 2032, 2033, 2034, 502, 310]
index2tags = collections.defaultdict(list)
index2name = collections.defaultdict(str)
stop_tags = ['技术服务', '技术转让', '技术交流', '技术开发']

tag2indices = collections.defaultdict(list)
edge_list = []
exist_cids = set()
with open(rawdata_path, 'r') as f:
    start = time.time()
    line_cur = 0
    cvecs = []
    for line in tqdm(f.readlines()):
        try:
            itemJson = json.loads(line)
        except json.decoder.JSONDecodeError:
            continue
        cid = None
        org_name = None
        if 'uid' in itemJson:
            cid = itemJson['uid']

        if cid in exist_cids or cid is None:
            continue
        else:
            exist_cids.add(cid)
        if 'name' in itemJson:
            org_name = itemJson['name']
        nickNames = itemJson['nickNames'] if 'nickNames' in itemJson else []
        tag_fields = itemJson['tags'] if 'tags' in itemJson else []
        if tag_fields is None:
            continue
        product_fields = itemJson['products'] if 'products' in itemJson else []
        tags = []
        for field in tag_fields:
            if 'type' not in field:
                continue
            source = field['type']
            if source not in USE_SOURCES:
                continue
            tags.extend(field['values'])
        tags = [t for t in tags if '公司' not in t and t not in stop_tags and len(t) > 2]
        if not tags:
            continue

        if org_name in node2idx:
            idx = node2idx[org_name]
        else:
            idx = len(node2idx) + 1
            node2idx[org_name] = idx

        for tag in tags:
            if tag in node2idx:
                t_idx = node2idx[tag]
            else:
                t_idx = len(node2idx) + 1
                node2idx[tag] = t_idx
            edge_list.append((idx, t_idx))

wf = codecs.open("../graph/new_small_top_raw.edgelist", mode='w')
for i, edge_ent in enumerate(edge_list):
    print(i, edge_ent)
    wf.write(f"{edge_ent[0]} {edge_ent[1]}\n")
wf.close()

idx_wf = codecs.open("../graph/new_small_top_raw.txt", mode='w')
for node, idx in node2idx.items():
    print(idx, node, index2name[idx])
    idx_wf.write(f"{idx}${node}\n")
idx_wf.close()
