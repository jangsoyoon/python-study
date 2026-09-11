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
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize
from konlpy.corpus import kolaw
from konlpy.tag import Komoran
from nltk.text import FreqDist
import matplotlib.pyplot as plt


# * 토큰(단어) 리스트를 받아서, n개씩 연속으로 묶은 튜플들의 리스트로 만들어주는 함수
# * 입력: 단어들이 쭉 나열된 리스트
# * 출력: n개씩 묶인 튜플들의 리스트
# * 원본 텍스트 → word_tokenize (단어로 자름) → ngram (n개씩 묶음) → FreqDist (빈도 셈)
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
# * lm2 는 2토큰으로 잘라서 lm2의 앞부분이 lm1의 단어들과 일치하는지 확인
# * Dict 의 구조
# print(dict(lm1), dict(lm2))
# print(lm1.most_common(10))
# print(lm2.most_common(10))
# print(lm2[("제1조", "①")])


def findKey(lm, *argv):
    return list(filter(lambda k: k[: len(argv)] == tuple(argv), lm.keys()))


#         조건식(k=dict의 key) k[:'법률이'1] == tuple('법률이'),       대상


# print(
#     findKey(lm1, "법률이"),
#     findKey(lm2, "법률이", "정하는"),
#     #   , findKey(lm2, "법률이")
# )
#! ###################################여기부터 다시###################################

# print(findKey(lm1, "법률이")[0])
# print(lm1[findKey(lm1, "법률이")[0]])
# P(?|법률이)  = P(법률이, 다음표현) / P(법률이)
#            = freq(법률이, 다음표현) / N
#            ---------------------------
#                   freq(법률이)/N

# * findKey의 리스트에서 해당 key에 해당하는 값을 lm2 dict 에서 찾아서 해당 value들(횟수)을 sum
# * -> 해당 key가 총 몇번 나왔는지 확인하기 위해서


# print(sum([lm2[key] for key in findKey(lm2, "법률이")]))
# {key:lm2[key] for key in findKey(lm2, '법률이')}
# * findKey(lm1, "법률이")[0] -> [0] 인 이유 : 값 자체가 [('법률이',)] 되어있어서 '법률이'를 뽑으려고
# * 리스트에서 key를 하나씩 꺼내면서, 그 key에 대해 계산식을 실행하고, {key: 계산결과} 형태로 딕셔너리를 만들어라
# * 여기서 계산결과 : lm2[key] / lm1[findKey(lm1, "법률이")[0]]
# * 법률이로 시작하는 각 조합(정하는/정한/확정된/헌법에)마다, 그 조합의 등장 횟수를 '법률이'의 전체 등장 횟수(57)로 나눠서 확률을 계산하고, {조합: 확률} 형태로 딕셔너리를 만들어라
# ! 질문: 근데 어차피 "법률이" 라는 걸로 찾을 걸 알면 굳이 findKey(lm1, "법률이") 을 할 필요가 없는데 왜 하는 걸까?
# ! -> 공통적으로 쓰기 위해서 findKey(lm2, "법률이") 와 통일시키기 위해서
# * -> ('법률이',)
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
# * 문장이 5단어라서, 그 사슬(연쇄법칙) 계산을 다 해내려면 최대 5개짜리 조합까지 세어봐야 하기 때문
# * 위에 "법률이" 같은 경우에는 Bigram(직전 1단어만 보는) 방식이었고 해당 방식은 전체 연쇄법칙(chain rule)이기 때문에
# * 그럼 아까 위에서도 (ngram(),3), (ngram(),4), (ngram(),5) 를 하면 됐을 일 아닌가?
# ! -> P(다음단어 | 법률이)   ← 조건이 항상 "법률이" 딱 1개 였기 때문에 Bigram 방식이라고 하는 것!!
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
# * 결과값 : 0.00021551724137931034
# ! 너무 작은데? -> 숫자 자체의 절대적인 크기는 별로 안 중요하고, 다른 문장과 비교했을 때 상대적으로 더 큰지 작은지가 중요하다
# ! 이 후보 vs 저 후보" 상대 비교가 N-gram 언어모델의 진짜 쓰임새
# ! 만약 2-gram으로 구한다고 하면,
# = P('.'|'민주공화국이다')P('민주공화국이다')
# = P('민주공화국이다'|'대한민국은')P('대한민국은')
# = P('대한민국은'|'①')P('①')
# = P('①'|'제1조')P('제1조')

p = 1.0
before = "제1조"
# lm1[findKey(lm1, before)[0]]
# ! 질문: 여기서 왜 [1:] 을 한거지?
# ! 밑에 corpus.splitlines()[6].strip()[1:] 이렇게 값을 모를 때 쓰려고..? -> yes
for key in ["제1조", "①", "대한민국은", "민주공화국이다", "."][1:]:
    p *= lm2[findKey(lm2, before, key)[0]] / lm1[findKey(lm1, before)[0]]
    before = key

# print(a)


# print(corpus.splitlines()[6].strip())
# 이 문장과 앞 문장 중 더 확률상 자연스러운 문장을 구하여라
# p = 1.0
# before = "②대한민국의"
# for key in word_tokenize(corpus.splitlines()[6].strip()[1:]):
#     p *= lm2[findKey(lm1, before, key)[0]] / lm1[findKey(lm1, before)[0]]
#     before = key

#######################################문장 생성##########################################
#! Language Generating 문장생성 => GPT(챗지피티 아님)
s = list()
key = "대한민국은"
s.append(key)
for i in range(20):
    keylist = findKey(lm2, key)
    candidates = {k: lm2[k] for k in keylist}
    # ! 왜 -1 이냐면 몇개짜리든 안전하게 마지막을 잡기 위해서
    key = sorted(candidates, key=candidates.get, reverse=True)[0][-1]
    s.append(key)
    # print(" ".join(s))
    # print(candidates)


# print(s)
s = list()
# * 1. 시작 문맥(2단어) 설정
key = (
    ("대한민국은", "민주공화국이다"),
    lm2[("대한민국은", "민주공화국이다")] / lm1[("대한민국은",)],
)
# key = (튜플,숫자) = (0:(단어,단어), 1:확률)
s.append(key)
# s[(key, key, ...)] = [t:(튜플,숫자),(튜플,숫자),(튜플,숫자)....]
# print(s)
# print(key)
# -> [(('대한민국은', '민주공화국이다'), 0.3333333333333333)]
for i in range(20):
    # * 2. 반복:
    # * a. 지금 문맥(2단어)으로 시작하는 3-gram 찾기
    # * b. 그 중 가장 빈도 높은 것 고르기
    # * c. 그 3-gram의 "뒤쪽 2단어"를 새 문맥으로 갱신
    # * d. 결과 저장
    # * e. (a로 돌아가서 반복)
    keylist = findKey(lm3, *key[0])
    # key[0] = (단어,단어)
    # *key[0] = 단어,단어
    # -> '대한민국은', '민주공화국이다'
    # keylist:[('대한민국은', '민주공화국이다', '.')]
    candidates = {k: lm3[k] for k in keylist}
    # candidates: {('대한민국은', '민주공화국이다', '.'): 1}
    key = sorted(candidates, key=candidates.get, reverse=True)[0]
    # candidates 의 확률이 제일 큰 걸로 정렬, 그리고 [0] 번째가 key
    # -> ('대한민국은', '민주공화국이다', '.')
    key = (key[-2:], (lm3[key] / lm2[key[-2:]]))
    # print(f"key:{key}")
    # -> (('민주공화국이다', '.'), 1.0)
    # 아까는 -1, bi-gram 바로 앞 단어만 체크하면돔
    # 지금은 -2, tri-gram 앞에 2단어를 줘야해서
    s.append(key)
    # print(candidates)
    # print(f"s:{s}")
    # print(f"s1:{s[0][0]}")
    # ! s[-1][0][-1] = s의 맨 마지막 원소의 [0]째의 마지막 원소 = ②대한민국의
    # print(f"s2:{s[-1][0][-1]}")
    # !s[0]: (대한민국은, 민주공화국이다)
    # !s[1]:            (민주공화국이다, .)          ← 앞 단어가 s[0]의 뒷 단어랑 겹침
    # !s[2]:                        (., ②대한민국의)  ← 앞 단어가 s[1]의 뒷 단어랑 겹침
    # !근데 이렇게만 하면, 맨 마지막 쌍의 "뒤쪽 단어"(가장 최신 단어인 ②대한민국의)는 어디에도 안 들어감. 왜냐면 그 단어는 아직 어떤 쌍의 "앞쪽"으로 쓰인 적이 없거든
    # !흘러온 단어들 + 아직 미처 못 넣은 맨 끝의 새 단어 = 완성된 문장
    # print(f'join:{" ".join([t[0][0] for t in s]) + " " + s[-1][0][-1]}')
# print(s)
print(" ".join([t[0][0] for t in s]) + " " + s[-1][0][-1])
# 대한민국은 민주공화국이다 . 다만 , 그

# 자동 띄어쓰기(       NLU      +      NLG) from LanguageModel(N-gram => LLM)
#           띄어쓰기가 있는지 확률  이해 띄어쓰기 추가
# !!!!!!!!!!!!!!! 여기부터 !!!!!!!!!!!!!!!
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

with sqlite3.connect("db/nlp/news.db") as con:
    cur = con.cursor()
    cur.execute("SELECT CONTENT FROM NEWS WHERE PK=?", [pk])
    s = cur.fetchone()[0]
    _, space = autoSpacing(re.sub(r"\s", "", s))
# print(space[:10])


#! 학습을 뉴스로 해보고 적용을 헌법으로 해보기
# ! LanguageModel => N-gram
# ! => NLU + NLG
# ! P(다음|given = 통계확률;데이터, 지금;잘주면됨 => RAG)
# ! N-gram; 1st Markov Assumption => Bi-gram, 2nd => Tri-gram...

#! Tokenizer => Token
#! 형태소, 음절 => 의미를 충분히 담고 있을까?


corpus = kolaw.open(kolaw.fileids()[0]).read()
ma = Komoran()
# print(ma.pos)

tokens = list(
    set([m[0] for m in ma.pos(re.sub(r"\s+", " ", corpus)) if m[1][0] in ["E", "J"]])
)

# print(len(tokens), tokens[:10])


def ngram2(s, n=2):
    gram = list()
    for i in range(len(s) - (n - 1)):
        gram.append(s[i : i + n])
    return gram


tokens = []
for term in word_tokenize(corpus):
    tokens.extend(ngram2(term, 3))
tokens = list(set(tokens))


# print(len(tokens), tokens[:10])
tokens = ngram([m for m in ma.pos(re.sub(r"\s+", " ", corpus))])
# print(len(tokens), tokens[:10])

# Tokenize => Stemming, Lemmatization
# stem = want, want[ed], want[s], ..

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

# print(stemmer.stem("i am going"))  # i am go
# for t in "want wants wanted".split():
#     print(t, stemmer.stem(t))
# want want
# wants want
# wanted want


# lemma => be = is, be, are

# [m for m in ma.pos("했다")]

# * Tokenization
# * word_tokenize, Stemming, Lemmatization, N-gram
# * 무게를 알 수 없는 공 8개 중에서 무게 하나가 다르다 양팔저울에서 몇번을 해야 다른 공을 찾아낼 수 있을까?
# * 3번 : (4/4) - (2/2) - (1/1) => log_2 = 8 = 3bits
# * 3번 : (3/3/3) - (1/1/1) => log_3
# * 비트수가 높음 => 정보량이 크구나 라고 추측할 수 있음
# * Entropy = 불확실성
# * -p log p
# * |
# * |       *
# * |    *     *
# * |  *         *
# * 0-------+-------- 동전의 앞면 p, 뒷면 1-p 앞면이 나올 확률이 0이라고 할 때 앞면은 0에 가깝고 뒷면은 1에 가깝다..
# * +:불확실성 제일 큰 지점
# * 하/어미(다/였다/였고/였는데/....=> 10)bits
# * 하였다/. => 1 bits
# * [분절]Subword-Tokenize; branching-entropy

tokens = FreqDist(word_tokenize(corpus))

candidate = list()
for key in tokens:
    if key[0] == "대":
        candidate.append(key)
candidate = list(set(candidate))

# print(candidate[:2])
# BrancingEntropy(대?) = -SIGMA(두번째음절) P(대,?)logP(대,?) 대 뒤에 무슨 글자가 나오는지 계산하기 위해서
# P(대,?) = P(?|대)P(대)
# = freq(대,?)/freq(대)*freq(대)/N
# => freq(대?)/freq(대)
from math import log

# freq(대)
freq1 = sum([tokens[t] for t in list(filter(lambda key: key[0] == "대", tokens))])

# freq(?|대) 를 구하기 위해, ? 의 종류를 찾음
second = list(set([t[1] for t in list(filter(lambda key: key[0] == "대", tokens))]))

entropy = 0.0
for c in second:
    freq2 = sum([tokens[t] for t in filter(lambda key: key[:2] == "대" + c, tokens)])
    # print(c, freq2, -(freq2/freq1)*log(freq2/freq1))
    entropy += -(freq2 / freq1) * log(freq2 / freq1)

# print(entropy)

from collections import defaultdict

# defaultdict(int)[1]
# defaultdict(lambda:0)[1]
# {}[1] => key error => key:int
# 절대로 key 에러가 나지 않음


# 특정 글자로 시작하는 모든 토큰들의 빈도를 누적하는 함수
def findKeyValue(key):
    result = defaultdict(lambda: 0)
    for k, v in tokens.items():
        if re.match(key, k):
            # if k.startswith(key)
            # if k[:len(key)] == key:
            result[k] = v
    return result


# print(findKeyValue("대"))


def branch(q):
    q = "대한민국임시정부의"
    branching = list()
    subwords = list()
    before = 1.0
    for i in range(1, len(q) + 1):
        # print(q[:i])
        rst = findKeyValue(q[:i])
        freq1 = sum(rst.values())
        entropy = {
            k: (freq2 / freq1) * log((freq2 / freq1)) for k, freq2 in rst.items()
        }
        branching.append(-sum(entropy.values()))
        if branching[-1] < before:
            # ! 1음절 제거, 치솟기 직전에 짤라야함
            # ! 대통령 + 이 -> 대통령 같은 단어들을 찾기 위해서 / 하나의 분절을 찾기 위해서
            before = branching[-1]
    return subwords


# for q in tokens.keys():
#     print((q, branch(q)))

q = "대한민국"
before = 0.0
for i in range(1, len(q)):
    # print(q[:i+1])
    freq2 = sum(findKeyValue(q[: i + 1]).values())
    freq1 = sum(findKeyValue(q[:i]).values())
    score = (freq2 / freq1) ** (-1 / i)
    # 응집력이 갈수록 떨어진다
    # if score > before:
    #     print(q[:i], freq1, freq2, freq2 / freq1, (freq2 / freq1) ** (-1 / i))
    before = score

new_tokens = list()
for q, v in tokens.items():
    # for q in tokens:
    before = 1.0
    result = []
    for i in range(1, len(q)):
        # print(q[:i+1])
        freq2 = sum(findKeyValue(q[: i + 1]).values())
        freq1 = sum(findKeyValue(q[:i]).values())
        score = (freq2 / freq1) ** (-1 / i)
        # 응집력이 갈수록 떨어진다
        if score > before and len(q[: i + 1]) > 1:
            # print(q[:i], freq1, freq2, freq2 / freq1, (freq2 / freq1) ** (-1 / i))
            # 딱 튀는 지점 있으면 break 할거임
            # 응집력 떨어졌다 올라가는 포인트 잡으려고 -> 뒤에 붙는 가지가 많다
            # 응집력.score > 직전.before , 분절(subword)의 길이가 1이 아닐 때만 토큰으로 추가하려고
            # result.append(q[: i + 1])
            # result.append({q[: i + 1]:v}) v를 같이 저장하거나
            result.extend([q[: i + 1]] * v)  # v를 곱하거나
            if len(q[i + 1 :]) > 1:
                # 분절 위치 다음부터 나머지까지가 있을 때만 토큰으로 추가하려고
                # result.append(q[i + 1 :])
                # result.append({q[i + 1 :]:v})
                result.extend([q[i + 1 :]] * v)
            break
        before = score

    # 응집력이 반등 안하면 비어있을 거임
    if len(result) == 0:
        # result.append(q)
        result.extend([q] * v)
    new_tokens.extend(result)

new_tokens = FreqDist(new_tokens)
# 유니크한 숫자가 줄었다
# -> 기존 토큰 대비 더 잘랐다 / 기존에 비해서 분절처리를 더 많이 했다
# new_tokens 전체 빈도 > 어절로 분리한 전체빈도
# new_tokens 유니크한 빈도 < 어절로 분리한 유니크한 빈도
# print(tokens.B(), new_tokens.B())
# ex) new_tokens.most_common() -> 국가로 시작하는 게(lemma) 22개나 된다
# print(list(zip(tokens.most_common(10), new_tokens.most_common(10))))
