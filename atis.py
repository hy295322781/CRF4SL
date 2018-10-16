# -*- coding:utf-8 -*-
"""
Created on 2018-10-16 21:28:34

Author: Xiong Zecheng (295322781@qq.com)
"""
import pickle
import pycrfsuite
import feature

class ATIS():
    def __init__(self,path):
        f = open(path, 'rb')
        try:
            self.train_set, self.valid_set, self.test_set, self.dicts = pickle.load(f, encoding='latin1')
        except:
            self.train_set, self.valid_set, self.test_set, self.dicts = pickle.load(f)
        f.close()
        self.__idx2words = dict()
        self.__idx2labels = dict()
        for key, value in self.dicts["words2idx"].items():
            self.__idx2words[value] = key;
        for key, value in self.dicts["labels2idx"].items():
            self.__idx2labels[value] = key;

    def train(self):
        trainer = pycrfsuite.Trainer(verbose=True)
        for i in range(len(self.train_set[0])):
            sentence = list(map(lambda x:self.__idx2words[x],self.train_set[0][i]))
            xseq = feature.sent2features(sentence)
            yseq = list(map(lambda y:self.__idx2labels[y],self.train_set[2][i]))
            trainer.append(xseq,yseq)
        trainer.train('ATIS.crfsuite')
        print("training success")

    def test(self):
        predicted_slot_count = 0
        actual_slot_count = 0
        hit_count = 0
        test_set_size = len(self.test_set[0])

        tagger = pycrfsuite.Tagger()
        tagger.open('ATIS.crfsuite')

        print("poccessing...")
        for i in range(test_set_size):
            if i != 0 and i % 100 == 0:
                print(str(i) + " done")
            sentence = list(map(lambda x: self.__idx2words[x], self.test_set[0][i]))
            predicted_seq = tagger.tag(feature.sent2features(sentence))
            predicted_slot = extract_slot(predicted_seq)

            label_seq = list(map(lambda x: self.__idx2labels[x], self.test_set[2][i]))
            actual_slot = extract_slot(label_seq)

            for item in predicted_slot:
                if item in actual_slot:
                    hit_count += 1
            predicted_slot_count += len(predicted_slot)
            actual_slot_count += len(actual_slot)

        print("test set size:" + str(test_set_size))
        print("predicted slot:" + str(predicted_slot_count) + " actual slot:" + str(actual_slot_count) + " hit:" + str(
            hit_count))
        print("Precision:" + str(hit_count / predicted_slot_count))
        print("Recall:" + str(hit_count / actual_slot_count))
        print("F1score:" + str(2 * hit_count / (actual_slot_count + predicted_slot_count)))

def extract_slot(seq):
    slot = list()
    i = 0
    while i < len(seq):
        if seq[i].startswith("B"):
            slot_type = seq[i][2:]
            l = 1
            while i + l < len(seq) and seq[i + l] == "I-" + slot_type:
                l += 1
            slot.append((i,slot_type,l))  # (槽的位置,槽的类型,槽的长度)
            i = i + l
        else:
            i += 1
    return slot

if __name__ == "__main__":
    atis = ATIS("data/atis.fold0.pkl")
    # atis.train()
    atis.test()
