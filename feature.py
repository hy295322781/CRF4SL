# -*- coding:utf-8 -*-
"""
Created on 2018-10-16 21:43:58

Author: Xiong Zecheng (295322781@qq.com)
"""
def word2features(sent,i):
    word = sent[i]
    features = [
        'word=' + word
    ]
    if i > 0:
        word1 = sent[i - 1]
        features.extend([
            'word-1=' + word1,
            'word-1|word=' + word1+'|'+word
        ])
    else:
        features.append('BOS')
    if i > 1:
        word2 = sent[i - 2]
        features.extend([
            'word-2=' + word2,
            'word-2|word-1=' + word2+'|'+word1
        ])
    if i < len(sent) - 1:
        word1 = sent[i + 1]
        features.extend([
            'word+1=' + word1,
            'word|word+1=' + word+'|'+word1
        ])
    else:
        features.append('EOS')
    if i < len(sent) - 2:
        word2 = sent[i + 2]
        features.extend([
            'word+2=' + word2,
            'word+1|word+2=' + word1+'|'+word2
        ])
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]