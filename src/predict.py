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

model = KeyedVectors.load_word2vec_format(args.output, binary=True, unicode_errors='ignore')
results = model.most_similar([8293])
print(results)
