# **新词发现算法**(**New Word Detection**)   

与 NCXavier 原本 repo 的区别 (Difference with the original fork):
1. 更新至python3 (Updated to python 3)
2. 针对原本就带 空格/符号/拆分符号 的语料做一些优化 (Optimize for corpus with space/split symbol)


**参考：**  
**Reference:**  
  - 算法（Algorithm）：
    - >http://www.matrix67.com/blog/archives/5044  
  - 代码（Code）：  
    - > https://github.com/xiulonghan/wordSeg     
    
    - > https://github.com/Moonshile/ChineseWordSegmentation  

**代码说明：**  
**Code describing:**  
- extract.py:  
    提供文档中所有成词的可能组合，以及计算词的点互信息时的一个组合。  
    Providing all possible word combines in document, and computing all word combines of PMI.  
 - entropy.py:  
    计算左右邻居熵的大小  
    Computing left and right entropy of neighbors  
- wordseg.py:  
    根据计算出的频数、点互信息和左右熵来找出成词可能的组合，最后与词典对比找出新词。  
    Finding all possible word combines by frequency, PMI and left/right entropy of neighbors, then comparing with diction to detect new word.  
