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

rawdata_path = '/Users/any/data/top_raw_small.json'
# rawdata_path = '/Users/any/data/top_raw.json'

idx2node = {}
node2idx = {}

index2tags = collections.defaultdict(list)
index2name = collections.defaultdict(str)
stop_tags = ['技术服务', '技术转让', '技术交流', '技术开发']

tag2indices = collections.defaultdict(list)
edge_list = []

with open(rawdata_path, 'r') as f:
    start = time.time()
    line_cur = 0
    cvecs = []
    for line in tqdm(f.readlines()):
        itemJson = json.loads(line)

        if 'id' in itemJson:
            cid = itemJson['id']
        if 'name' in itemJson:
            name = itemJson['name']
        if 'sample' not in itemJson:
            continue
        sampleJsonStr = itemJson['sample']
        sampleJson = json.loads(sampleJsonStr)
        if "fields" not in sampleJson:
            continue
        fields = sampleJson['fields']
        tags = []
        for field in fields:

            if 'type' not in field:
                continue
            if 'text' != field['type']:
                continue
            source = field['name']
            if source == "202":
                # print(name, field)
                vals = field['value']
                tags.extend(vals)

        tags = [t for t in tags if '公司' not in t and t not in stop_tags]
        if not tags:
            continue

        if name in node2idx:
            idx = node2idx[name]
        else:
            idx = len(node2idx) + 1
            node2idx[name] = idx

        for tag in tags:
            if tag in node2idx:
                t_idx = node2idx[tag]
            else:
                t_idx = len(node2idx) + 1
                node2idx[tag] = idx
            edge_list.append((idx, t_idx))

wf = codecs.open("../graph/small_top_raw.edgelist", mode='w')
for i, edge_ent in enumerate(edge_list):
    print(i, edge_ent)
    wf.write(f"{edge_ent[0]} {edge_ent[1]}\n")
wf.close()

idx_wf = codecs.open("../graph/small_top_raw.txt", mode='w')
for node, idx in node2idx.items():
    print(idx, node, index2name[idx])
    idx_wf.write(f"{idx} {node}\n")
idx_wf.close()
