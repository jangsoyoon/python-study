#####################################################################
#! 한 단어를 => 여러개의 분절로
#! 한 어절을 => 여러개의 분절로
#! def BPE(tokens):
#!     while N <w 적당한 숫자:
#!         (음절단위)Bi-gram = 쌍을 찾아야함 (한 어절에서 나온 이웃한 음절쌍)
#!                 max = 쌍 중에 가장 많이 나온 애를 찾아야함
#!         replace, re.sub = 가장 많이 나온 애 => 짧은 걸로 replace 함
#!                             (A, B) = AB
#####################################################################
import re
from sqlite3 import SQLITE_DBCONFIG_ENABLE_FTS3_TOKENIZER

from numpy import vectorize

corpus = """
low low low low low
lower lower
newest newest newest newest newest newest
widest widest widest
"""


def preprocessing(d):
    # {'토 큰': 빈도}
    tokens = {}
    for token in d.split():
        token = " ".join(token) + " </w>"
        if token not in tokens:
            tokens[token] = 0
        tokens[token] += 1
    return tokens


# print(preprocessing(corpus))


def get_stats(vocab):
    # ('t o k e n </w>':3) => ('t o':3, 'o k': 3, 'k e':3, ...)
    tokens = {}
    n = 2  # bi-gram이라서 (pair만 필요해서)
    for token, freq in vocab.items():
        s = token.split()
        for i in range(len(s) - (n - 1)):
            token = " ".join(s[i : i + n])
            # tokens 에 지금 비어있기 때문에 tokens에 아무것도 없다면 token key 를 집어넣기 위해
            if token not in tokens:
                tokens[token] = 0
            tokens[token] += freq

    return tokens


vocab = preprocessing(corpus)
# print(f"vocab:{vocab}")
pairs = get_stats(vocab)
best = max(pairs, key=pairs.get)
# print(f"best:{best}")
# print(best, pairs['e s'])


def merge_vocab(be, vo):
    tokens = {}
    for k, v in vo.items():
        new_key = re.sub(be, be.replace(" ", ""), k)
        tokens[new_key] = v

    return tokens


# print(merge_vocab(best, vocab))


for i in range(5):
    pairs = get_stats(vocab)
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)


# print(sum([len(k.split()) for k in vocab]))

# print(
#     len(list(set([t for k in vocab for t in k.split()]))) - 1,
#     list(set([t for k in vocab for t in k.split()])),
# )
# print(
#     len(list(set(" ".join(preprocessing(corpus).keys()).split()))) - 1,
#     list(set(" ".join(preprocessing(corpus).keys()).split())),
# )


#! 텍스트 데이터 => Encoding(카테고리형 데이터 -> 수치형 데이터) => Vectorize
#!                             ------- => 어떤 게 있느냐? => NLP + 언어학

#! 문서 = 1문단 = 1문장 => sent_tokenize
#! 문장 구성 = 단어(어절)들로 => word_tokenize
#!              = 다른 패턴 => regexp_tokenize
#!              = 감정 표현 => TweetTokenize
#! (교착어) = 어절 = 형태소들 => 형태소분석기(형태학적 / 언어학적 지식) Morphological +  통사 + 구문 ...
#!   통계        perplexity, entropy => BranchingEntropy, Perplexity(PPL) 분기점을 찾을려고 한 것
#! 이웃한 표현; collocation(연어) => Ngram + Ngram LM
#!   통계; 가장 많이 나온 쌍을 한 토큰 => BPE
#! ========================= Feature Candidates Extraction ========================= Zipf, Heaps
#! 정규화(Normalization) => 같은 형태, 모습, 의미 토큰들로 변환, ex. Ph.D, D.C, H.P, KU, ....)
