# -*- coding: utf-8 -*-
"""
@author: zhangzhen
@software: PyCharm
@file: predict.py
@time: 2022/5/12 11:19
"""
from gensim.models import KeyedVectors
from src import parse_args

args = parse_args()
target_idx = 8293

model = KeyedVectors.load_word2vec_format(args.output, binary=True, unicode_errors='ignore')
results = model.most_similar([target_idx])
idx2node = {}
with open("graph/small_top_raw.txt", mode='r') as f:
    for line in f.readlines():
        idx, name = line.strip().split("$")
        idx2node[int(idx)] = name

print(results)
for ent in results:
    idx = ent[0]
    sim = ent[1]
    print(idx2node[idx], sim)
