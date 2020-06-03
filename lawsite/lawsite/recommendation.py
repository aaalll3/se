import pickle
import jieba
import re
import numpy as np
from collections import Counter
from typing import *

"""
recommendation: Dict[str, List[str]]
键和值均为 xml 的路径，格式为
'xml_3.zip/xml_3/925f8666-2ce5-4463-a9bd-e34d8293d807/0229a1fb762215e6953779da08c9e59b070.xml'
"""
recommendation = pickle.load(open('lawsite/data/recommendation', 'rb'))

data = pickle.load(open('lawsite/data/data', 'rb'))
tree = pickle.load(open('lawsite/data/tree', 'rb'))
informative_words = pickle.load(open('lawsite/data/informative_words', 'rb'))[:2000]
word_map = {word: index for index, word in enumerate(informative_words)}
word_count = pickle.load(open('lawsite/data/word_count', 'rb'))
pca = pickle.load(open('lawsite/data/pca', 'rb'))
paths = pickle.load(open('lawsite/data/paths', 'rb'))


def search_text(text: str, count: int = 10) -> Tuple[List[str], str]:
    """
    对于指定的文书，返回一些推荐
    :param text: 文书
    :param count: 推荐数量
    :return: 一些推荐的 xml 地址，可能的案件类型（例如 '贩卖毒品罪'）
    """
    tfidf = np.zeros((1, len(informative_words)))
    for word, freq in Counter(jieba.lcut(re.sub(r'\s', '', text))).most_common(1000):
        index = word_map.get(word)
        if index is not None:
            tfidf[0][index] = freq / len(text) / word_count[word]
    decomp = pca.transform(tfidf)
    nearest = tree.query(decomp, k=max(count, 10) + 1)[1][0][1:]
    possible_tag = Counter(tag for i in nearest[:10] for tag in data[i]['tag'])
    return [paths[i] for i in nearest[:count]], possible_tag.most_common(1)[0][0]
