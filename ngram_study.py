# N-Gram => nth MarkovAssumption
# next letter = SLM(given = t1, t2, t3, t4=음절)
# token_i = P(ti|t1,t2,t3,t4)
#           P(t1,t2,t3,t4,ti) ==> /bt1t2t3t4ti/b
#           -----------------
#           P(t1,t2,t3,t4)    ==> /bt1t2t3t4/b => 전체 중에 t1t2t3t4의 상대적 빈도(비율) MLE
#                             ==> /b(?=11,172개정도,?,?,?)/b
# P(?=고|고려대학) => P(고,려,대,학)
#               => P(학|고,려,대)P(고,려,대)
#               => P(대|고,려)P(고,려)
#               => P(려|고)P(고)
# ---------------> ChainRule
# Bi-Gram = 2-Gram
#               => P(?=고|고려대학) => P(고,려,대,학)
#               => P(학|대)
#               => P(대|려)
#               => P(려|고)P(고)
# P(A,B) = P(B|A)P(A) // P(A|B) = P(A와 B가 같이 일어날 확률) / P(B가 일어날 확률)
from gettext import find

from matplotlib.backend_bases import key_press_handler
from nltk.collocations import BigramCollocationFinder
from konlpy.corpus import kolaw
from nltk.tokenize import word_tokenize
from nltk.text import FreqDist


def ngram(tokens, n=2):
    gram = list()
    for i in range(len(tokens) - (n - 1)):
        gram.append(tuple(tokens[i : i + n]))
    return gram


# print(ngram("가나다라마바사", 1))
# print(BigramCollocationFinder.from_words("가나다라마바사").__dict__["ngram_fd"])

# P(법률이)  = freq(법률이)
#!  Language Understanding = Natural Language Prob. => Bert
corpus = kolaw.open(kolaw.fileids()[0]).read()
lm1 = FreqDist(ngram(word_tokenize(corpus), 1))
lm2 = FreqDist(ngram(word_tokenize(corpus)))

# print(dict(lm1), dict(lm2))
# print(lm1.most_common(10))
# print(lm2.most_common(10))


def findKey(lm, *argv):
    return list(filter(lambda k: k[: len(argv)] == tuple(argv), lm.keys()))


#         조건식(k=dict의 key) k[:'법률이'1] == tuple('법률이'),       대상


print(
    findKey(lm1, "법률이"),
    findKey(lm2, "법률이", "정하는"),
    #   , findKey(lm2, "법률이")
)

# P(?|법률이)  = P(법률이, 다음표현) / P(법률이)
#            = freq(법률이, 다음표현) / N
#            ---------------------------
#                   freq(법률이)/N

# sum([lm2[key] for key in findKey(lm2, '법률이')])
# {key:lm2[key] for key in findKey(lm2, '법률이')}
# print(
#     {key: lm2[key] / lm1[findKey(lm1, "법률이")[0]] for key in findKey(lm2, "법률이")}
# )
# print(
#     sum(
#         {
#             key: lm2[key] / lm1[findKey(lm1, "법률이")[0]]
#             for key in findKey(lm2, "법률이")
#         }.values()
#     )
# )

a = corpus.splitlines()[5].strip()
# 이 문장의 확률을 구하여라
# P('제1조', '①', '대한민국은', '민주공화국이다', '.')
# = P('.'|'제1조', '①', '대한민국은', '민주공화국이다')P('제1조', '①', '대한민국은', '민주공화국이다')
#   P('민주공화국이다'|'제1조', '①', '대한민국은')P('제1조', '①', '대한민국은')
#   P('대한민국은'|'제1조', '①')P('제1조', '①')
#   P('①'|'제1조')P('제1조')
# P('제1조') = freq('제1조') / N
# P('①'|'제1조') = P('제1조', '①')/P('제1조') = (freq('제1조', '①')/N) / (freq('제1조')/N)
lm3 = FreqDist(ngram(word_tokenize(corpus), 3))
lm4 = FreqDist(ngram(word_tokenize(corpus), 4))
lm5 = FreqDist(ngram(word_tokenize(corpus), 5))

# P('제1조') = freq('제1조') / N
p = 1.0
p *= lm1[("제1조",)] / lm1.N()
# P('①'|'제1조') = P('제1조', '①')/P('제1조') = (freq('제1조', '①')/N) / (freq('제1조')/N)
p *= lm2[findKey(lm2, "제1조", "①")[0]] / lm1[("제1조",)]
p *= lm3[findKey(lm3, "제1조", "①", "대한민국은")[0]] / lm2[("제1조", "①")]
p *= (
    lm4[findKey(lm4, "제1조", "①", "대한민국은", "민주공화국이다")[0]]
    / lm3[("제1조", "①", "대한민국은")]
)
p *= (
    lm5[findKey(lm5, "제1조", "①", "대한민국은", "민주공화국이다", ".")[0]]
    / lm4[("제1조", "①", "대한민국은", "민주공화국이다")]
)
# print(p)
# ! 만약 2-gram으로 구한다고 하면,
# = P('.'|'민주공화국이다')P('민주공화국이다')
# = P('민주공화국이다'|'대한민국은')P('대한민국은')
# = P('대한민국은'|'①')P('①')
# = P('①'|'제1조')P('제1조')

# p = 1.0
# before = "제1조"
# lm1[findKey(lm1, before)[0]]
# for key in ["제1조", "①", "대한민국은", "민주공화국이다", "."][1:]:
#     p *= lm2[findKey(lm1, before, key)[0]] / lm1[findKey(lm1, before)[0]]
#     before = key

# print(a)


corpus.splitlines()[6].strip()
# d이 문장과 앞 문장 중 더 확률상 자연스러운 문장을 구하여라
# p = 1.0
# before = "②대한민국의"
# for key in word_tokenize(corpus.splitlines()[6].strip()[1:]):
#     p *= lm2[findKey(lm1, before, key)[0]] / lm1[findKey(lm1, before)[0]]
#     before = key


#! Language Generating 문장생성 => GPT(챗지피티 아님)
s = list()
key = "대한민국은"
s.append(key)
for i in range(20):
    keylist = findKey(lm2, key)
    candidates = {k: lm2[k] for k in keylist}
    key = sorted(candidates, key=candidates.get, reverse=True)[0][-1]
    s.append(key)
    # print(" ".join(s))
    # print(candidates)


s = list()
key = (
    ("대한민국은", "민주공화국이다"),
    lm2[("대한민국은", "민주공화국이다")] / lm1[("대한민국은",)],
)
# key = (튜플,숫자) = (0:(단어,단어), 1:확률)
s.append(key)
# s[(key, key, ...)] = [t:(튜플,숫자),(튜플,숫자),(튜플,숫자)....]
for i in range(20):
    keylist = findKey(lm3, *key[0])
    # key[0] = (단어,단어)
    # *key[0] = 단어,단어
    candidates = {k: lm3[k] for k in keylist}
    key = sorted(candidates, key=candidates.get, reverse=True)[0]
    key = (key[-2:], lm3[key] / lm2[key[-2:]])
    # 아까는 -1, bi-gram 바로 앞 단어만 체크하면돔
    # 지금은 -2, tri-gram 앞에 2단어를 줘야해서
    s.append(key)
    # print(candidates)
# print(" ".join([t[0][0] for t in s]) + " " + s[-1][0][-1])
# 대한민국은 민주공화국이다 . 다만 , 그

# 자동 띄어쓰기(       NLU      +      NLG) from LanguageModel(N-gram => LLM)
#           띄어쓰기가 있는지 확률  이해 띄어쓰기 추가
import re

s = "제1조 ① 대한민국은 민주공화국이다."
s = re.sub(r"\s", "", s)
# print(s)
"제1조①대한민국은민주공화국이다."
from collections import Counter

p1 = (re.compile(r"\n\n"), "\n")
p2 = (re.compile(r"(?:\t|[ ])+"), " ")
p3 = (re.compile(r"^\s+|\s+$"), "")

for p in [p1, p2, p3]:
    corpus = p[0].sub(p[1], corpus)

gram1 = Counter(ngram(corpus, 1))
gram2 = Counter(ngram(corpus, 2))
gram3 = Counter(ngram(corpus, 3))
gram4 = Counter(ngram(corpus, 4))
gram5 = Counter(ngram(corpus, 5))
from nltk.tokenize import sent_tokenize

s = sent_tokenize(corpus)[5]
s = re.sub(r"\s", "", s)
# print(s)

result = ""
for c in s:
    if len(result) < 3:
        result += c
        continue

    #!!!!!!!!!!!!   숫자 바꿔가면서 결과 한번 보기    !!!!!!!!!!!!
    # keys = findKey(gram2, *tuple(result[-1:]))
    # keys = findKey(gram3, *tuple(result[-2:]))
    keys = findKey(gram4, *tuple(result[-3:]))
    candidates = dict()
    # keys = [(첫음절, 두번째음절), (첫음절, 두번째음절), (첫음절, 두번째음절)...]
    # freq2 = gram1[tuple(result[-1:])]
    # freq2 = gram2[tuple(result[-2:])]
    freq2 = gram3[tuple(result[-3:])]
    for key in keys:
        # freq1 = gram2[key]
        # freq1 = gram3[key]
        freq1 = gram4[key]
        prob = freq1 / freq2
        candidates[key] = prob
    if len(keys) == 0:
        next = "갈"
    else:
        next = sorted(candidates, key=candidates.get, reverse=True)[0][-1]

    if next == " ":
        result += " "
    result += c
# print(s, result)

from nltk.tokenize import sent_tokenize

s = sent_tokenize(corpus)[5]
s = re.sub(r"\s", "", s)
# print(s)


def autoSpacing(s):
    no2gram = {0: gram1, 1: gram2, 2: gram3, 3: gram4, 4: gram5}

    result = ""
    for c in s:
        if len(result) < 3:
            result += c
            continue

        candidates = dict()
        for i in range(1, len(result[-max(no2gram.keys()) :]) + 1):
            # result='음절'    i = 1,2 , range(1, 3)
            keys = findKey(no2gram[i], *tuple(result[-i:]))
            freq2 = no2gram[i - 1][tuple(result[-i:])]
            for key in keys:
                freq1 = no2gram[i][key]
                prob = freq1 / freq2
            candidates[key] = prob

        if len(candidates) == 0:
            next = "갈"
        else:
            next = sorted(candidates, key=candidates.get, reverse=True)[0][-1]

        if next == " ":
            result += " "
        result += c
    return s, result


# print(autoSpacing(s))
# ('제3조대한민국의영토는한반도와그부속도서로한다.', '제3조 대한민국 의영토는 한반도와 그 부속도서로 한다.')
import sqlite3

pk = 50

with sqlite3.connect("news.db") as con:
    cur = con.cursor()
    cur.execute("SELECT CONTENT FROM NEWS WHERE PK=?", [pk])
    s = cur.fetchone()[0]
    _, space = autoSpacing(re.sub(r"\s", "", s))
# print(space[:10])


#! 학습을 뉴스로 해보고 적용을 헌법으로 해보기
