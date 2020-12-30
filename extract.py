# -*- coding: utf-8 -*-
import os
import re


def extract_cadicateword(_doc,_max_word_len):
    indexes = []
    doc_length = len(_doc)
    for i in range(doc_length):
        for j in range(i+1, min(i+1+_max_word_len,doc_length+1)):
            skip_flag = False
            for k in range(i, j):
                if _doc[k] == " ":
                    skip_flag = True
                    break
            if not skip_flag:
                indexes.append((i, j))
    return sorted(indexes, key = lambda _word:_doc[_word[0]:_word[1]])

def gen_bigram(_word_str):
    '''
    A word is divide into two part by following all possible combines.
    For instance, ABB can divide into (a,bb),(ab,b)
    :param _word_str:
    :return:
    '''
    return [(_word_str[0:_i],_word_str[_i:]) for _i in range(1,len(_word_str))]
