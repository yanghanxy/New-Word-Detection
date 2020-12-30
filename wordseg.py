#-*- coding:utf-8 -*-
"""
Chinese word segmentation algorithm with corpus
Author: "Xylander"
"""


import os
import re
import math
import time
from entropy import compute_entropy
from extract import extract_cadicateword,gen_bigram
import pandas as pd
import codecs


class wordinfo(object):
    '''
    Record every candidate word information include left neighbors, right neighbors, frequency, PMI
    '''
    def __init__(self,text):
        super(wordinfo,self).__init__()
        self.text = text
        self.freq = 0.0
        self.left = []  #record left neighbors
        self.right = [] #record right neighbors
        self.pmi = 0

    def update_data(self,left,right):
        self.freq += 1.0
        if left:
            self.left.append(left)
        if right:
            self.right.append(right)

    def compute_indexes(self,length):
        #compute frequency of word,and left/right entropy
        self.freq /= length
        self.left = compute_entropy(self.left)
        self.right = compute_entropy(self.right)

    def compute_pmi(self,words_dict):
        #compute all kinds of combines for word
        sub_part = gen_bigram(self.text)
        if len(sub_part) > 0:
            self.pmi = min(map(lambda word : math.log(self.freq/words_dict[word[0]].freq/words_dict[word[1]].freq),sub_part))

class segdocument(object):
    '''
    Main class for Chinese word segmentation
    1. Generate words from a long enough document
    2. Do the segmentation work with the document
    reference:

    '''
    def __init__(self,doc,max_word_len=5,min_tf=0.000005,min_entropy=0.07,min_pmi=6.0):
        super(segdocument,self).__init__()
        self.max_word_len = max_word_len
        self.min_tf = min_tf
        self.min_entropy = min_entropy
        self.min_pmi = min_pmi
        #analysis documents
        self.word_info = self.gen_words(doc)
        count = float(len(self.word_info))
        self.avg_frq = sum(map(lambda w : w.freq,self.word_info))/count
        self.avg_entropy = sum(map(lambda w : min(w.left,w.right),self.word_info))/count
        self.avg_pmi = sum(map(lambda w:w.pmi,self.word_info)) / count
        filter_function = lambda f:len(f.text) > 1 and f.pmi > self.min_pmi and f.freq > self.min_tf\
                                   and min(f.left,f.right) > self.min_entropy
        self.word_tf_pmi_ent = map(lambda w :(w.text,len(w.text),w.freq,w.pmi,min(w.left,w.right)),filter(filter_function,self.word_info))

    def gen_words(self,doc):
        #pattern = re.compile('[：“。”，！？、《》……；’‘\n——\r\t）、（——^[1-9]d*$]')
        #pattern = re.compile('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?：、~@#”“￥：%……&*（）]+|[[A-Za-z0-9]*$]'.decode('utf-8'))
        pattern = re.compile(u'[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!@#$%^&*\\-_=+a-zA-Z，。《》、？：；“”‘’｛｝【】（）…￥！—┄－]+')
        doc = pattern.sub(' ',doc)
        word_index = extract_cadicateword(doc,self.max_word_len)
        word_cad = {} #后选词的字典
        for suffix in word_index:
            word = doc[suffix[0]:suffix[1]]
            if word not in word_cad:
                word_cad[word] = wordinfo(word)
                # record frequency of word and left neighbors and right neighbors
            word_cad[word].update_data(doc[suffix[0]-1:suffix[0]],doc[suffix[1]:suffix[1]+1])
        length = len(doc)
            #computing frequency of candicate word and entropy of left/right neighbors
        for word in word_cad:
            word_cad[word].compute_indexes(length)
        #ranking by length of word
        values = sorted(word_cad.values(),key=lambda x:len(x.text))
        for v in values:
            if len(v.text) == 1:
                continue
            v.compute_pmi(word_cad)
        # ranking by freq
        return sorted(values,key = lambda v: len(v.text),reverse = False)


if __name__ == '__main__':
        starttime = time.clock()
        path = os.path.abspath('.')
        wordlist = []
        word_candidate = []
        dict_bank = []
        dict_path = path + '\\dict.txt'

        doc = codecs.open(path+'\\train_for_ws.txt', "r", "utf-8").read()

        word = segdocument(doc,max_word_len=3,min_tf=(1e-08),min_entropy=1.0,min_pmi=3.0)
        print('avg_frq:'+ str(word.avg_frq))
        print('avg_pmi:' + str(word.avg_pmi))
        print('avg_entropy:'+ str(word.avg_entropy))

        for i in codecs.open(dict_path, 'r', "utf-8"):
            dict_bank.append(i.split(' ')[0])

        print('result:')
        for i in word.word_tf_pmi_ent:
            if i[0] not in dict_bank:
                word_candidate.append(i[0])
                wordlist.append([i[0],i[1],i[2],i[3],i[4]])
                
        # ranking on entropy (primary key) and pmi (secondary key)
        wordlist = sorted(wordlist, key=lambda word: word[3], reverse=True)
        wordlist = sorted(wordlist, key=lambda word: word[4], reverse=True)
        
        seg = pd.DataFrame(wordlist,columns=['word','length','fre','pmi','entropy'])
        seg.to_csv(path+'/extractword.csv', index=False ,encoding="utf-8")

        # intersection = set(word_candidate) & set(dict_bank)
        # newwordset = set(word_candidate) - intersection
        
        # for i in wordlist:
        #     print(i[0],i[1],i[2],i[3],i[4])

        endtime = time.clock()
        print(endtime-starttime)
        
