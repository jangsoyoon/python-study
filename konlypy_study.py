# [전처리]
# (텍스트-자연어) 데이터
#      => 언어모델(LM) 모사(계산 가능한 모델 -통계/확률)
#      화용/담화분석 => 의미분석 => 구문분석 => 형태소분석
#      문단/문서        문장      구절,품사    형태소
#                                         Token(izing)
#                                         Vector(izing)

# [토큰] ==> FeatureExtraction + BPE => FeatureSelection(Normalization)
# 음절, 음절들 => 어절, 어절들 => 문장, 문장들 => 문단, 문단들 => 문서
# Morpheme           ParseTree(Grammar)
# 형태소 => 단어, 단어들 => 구, 절  구,절=> 문장 문장들 => 문단
#  Stemming             Lemmatiztion
# 어간(stem) + 어미,        어근(lemma) + 접사
# [있]+다/는데/있고....     접두 + [] + 접미
# 문장 ㅌ 문단 ㅌ 문서
from multiprocessing import heap
from os import name
import sqlite3

from konlpy.tag import Kkma, Hannanum, Komoran, Okt
from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize, TweetTokenizer
from nltk.corpus import gutenberg
import nltk
from nltk.text import Text
from string import punctuation
from nltk.text import FreqDist
from regex import R

# nltk.download("punkt_tab")
corpus = gutenberg.open(gutenberg.fileids()[0]).read()
# len(corpus.splitlines()), len(sent_tokenize(corpus))
news = """박진영의 JYP엔터테인먼트(JYP Ent)가 최근 증권사 목표주가 하향 리포트가 가장 많이 나온 종목으로 집계됐다. 국내 증시 변동성이 커지며 목표주가를 낮춘 보고서가 늘어난 가운데, JYP Ent는 개별 종목 기준 하향 리포트 28건으로 가장 많았다."""
# print(sent_tokenize(news)[1])

s = '국내 증시 "변동성이" 커지며 목표주가를 낮춘 보고서가 늘어난 가운데, JYP... Ent는 개별 . . .종목 기준 하향 리포트 28건으로 가장 많았다.'
# print(sent_tokenize(s))
# ...=> 문장 내 상관x
# . . . => [.?!] + whitespace => 문장으로 끊어냄
# 어절(단어) ㅌ            문장 ㅌ 문단 ㅌ 문서
# word_tokenize         sent_tokenize => 문장을 쪼갤 때 유용한 기능

# print(len(set(news.split())), len(set(word_tokenize(news))))
# print(len(regexp_tokenize(corpus, r"\b(\w+)\b")))

# print(len(TweetTokenizer().tokenize(corpus)))
emma = Text(word_tokenize(corpus))
# UniqueToken수    #전체 Token수
# 어휘, 용어, Term
# emma.vocab().B(), emma.vocab().N()
# print(emma.vocab().most_common(10))
# print(emma.tokens[:10], corpus[:10])
# nltk.download("draw")
# print(emma.collocation_list())
# 빈도
# emma.count('Mr.'), emma.count('Knightley')
# 비율 입력토큰의수/전체토큰수 => MLE 확률
# emma.vocab().freq('Mr.'), emma.vocab().freq('Knightley')
# print(emma.vocab().freq(","))
# print(emma.concordance("Emma"))
# print(emma.dispersion_plot(["Emma", "Knightley"]))

from konlpy.corpus import kobill, kolaw

kcorpus = kolaw.open(kolaw.fileids()[0]).read()
# print(len(kcorpus.splitlines()), len(sent_tokenize(kcorpus)))
# print(len(kcorpus.split()), len(word_tokenize(kcorpus)))
# print(len(set(kcorpus.split())), len(set(word_tokenize(kcorpus))))
# print(len(word_tokenize(kcorpus)) / len(set(word_tokenize(kcorpus))))
law = Text(word_tokenize(kcorpus))
# print(law.collocations())
# print(law.vocab().most_common(50))
# print(law.similar("법률이", 5))
from nltk.tag import pos_tag
from nltk.help import upenn_tagset, brown_tagset

# Tagset = 품사표
# Upenn = Univ of 펜실베니아
# nltk.download("tagsets_json")
# nltk.download("averaged_perceptron_tagger_eng")
# print(pos_tag(word_tokenize(sent_tokenize(corpus)[1]))[:4])
# print(upenn_tagset("PRP"), upenn_tagset("VBD"))

# emma_pos1 = Text(pos_tag(word_tokenize(corpus)))
# emma_pos2 = Text([pos[0] for pos in pos_tag(word_tokenize(corpus))])

# print(emma.vocab().N(), emma_pos1.vocab().N(), emma_pos2.vocab().N())
# print(emma.vocab().B(), emma_pos1.vocab().B(), emma_pos2.vocab().B())

# word_tokenize => 구두점, (분리)어절 = 단어(형태소분석)
from konlpy.tag import Hannanum, Kkma, Komoran, Okt

ma = [Hannanum(), Kkma(), Komoran(), Okt()]
s = sent_tokenize(kcorpus)[1]
# 형태소분석기, morph = 형태소, pos = (형태소, 품사), noun = 명사
# for tag, name in zip(ma, ["Hannanum", "Kkma", "Komoran", "Okt"]):
#     print(name, len(tag.morphs(s)), len(tag.morphs(s)) / len(s.split()))
#     print(tag.morphs(s))
#     print(
#         list(
#             map(lambda tokens: (tokens[0], tag.tagset.get(tokens[1], "X")), tag.pos(s))
#         ),
#         end="\n\n",
#     )

# tag.tagset
import re

s = re.sub(r"\s", "", s)
# ! Komoran 이 낫다.
# for tag, name in zip(ma, ["Hannanum", "Kkma", "Komoran", "Okt"]):
#     print(name, len(tag.morphs(s)), len(tag.morphs(s)) / len(s.split()))
#     print(tag.morphs(s))
#     print(
#         list(
#             map(lambda tokens: (tokens[0], tag.tagset.get(tokens[1], "X")), tag.pos(s))
#         ),
#         end="\n\n",
#     )

# from konlpy.tag import Mecab
from mecab import MeCab

# ma_mecab = MeCab()  # 은전한닢


# print(ma_mecab.pos(s.replace(" ", "")))

# law1 = Text(ma[2].morphs(kcorpus))
# law2 = Text(ma[2].pos(kcorpus))

# print(law.vocab().N(), law1.vocab().N(), law2.vocab().N())
# print(law.vocab().B(), law1.vocab().B(), law2.vocab().B())

# law1.collocations()  # Ngram
# print(law1.similar("헌법")) # 통계량; Chi, PMI

from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures

# bigram = BigramCollocationFinder.from_words(law1.tokens)
# print(bigram.nbest(BigramAssocMeasures.pmi, 10))

# ! 경험적법칙 = Zipf's 법칙 => 최빈도 = 그 다음빈도x2, 순위의 역순 = 고빈도순으로 나열// 즉, 1위가 있으면 2위의 2배라는 말.. / 빈도가 낮아지는 방향 = 순위 숫자가 커지는 방향
# ! 그니까 순위의 역순 = 고빈도순으로 나열이라는 것이 그냥 순위가 커질수록 빈도가 낮아진다 라는 뜻임
# 가장 많이 나온 토큰은 그 다음 많이 나온 토큰의 약 2배다
# 빈도 순서대로 나열 = 순위의 역순

emma_tokens = dict(map(lambda token: (token, emma.count(token)), set(emma.tokens)))

import matplotlib.pyplot as plt

# 빈도 큰 순서대로 나열(단, 정규화만 0~1)
keys = sorted(emma_tokens, key=emma_tokens.get, reverse=True)[:10]
values = [emma_tokens[key] / max(emma_tokens.values()) for key in keys]
# 순위의 역순으로 나열(1~0)
ordered = [1 / (i + 1) for i in range(len(keys))]

# plt.plot(range(len(keys)), values, c="r")
# plt.plot(range(len(keys)), ordered, c="b")
# plt.xlim(0, 100)
# plt.show()


raw_emma = gutenberg.open(gutenberg.fileids()[0]).read()
raw_emma = gutenberg.open(gutenberg.fileids()[0]).read().lower()
# 대소문자 구별 X
# (8406, 72어쩌구)
text1_emma = Text(word_tokenize(raw_emma))  # 구두점 포함
text2_emma = FreqDist(regexp_tokenize(raw_emma, r"\b(\w+)\b"))  # 구두점 제외
# print(text1_emma.vocab().B(), text2_emma.B())
# print(text1_emma.vocab().N(), text2_emma.N())

N = 100
# Text.FreqDist() = vocab() => Counter => Dict.max() => Dict.Key
# FreqDist[Key=text1_emma.max()] / text1_emma.vocab() 의 value 가 가장 많은 키를 찾은 거임
max1_emma = text1_emma.vocab()[text1_emma.vocab().max()]
max2_emma = text1_emma.vocab()[text2_emma.max()]
freq1_emma = [row[1] / max1_emma for row in text1_emma.vocab().most_common(N)]
# => Sorted => [(k1,v1), (k2, v2), ...] X N
freq2_emma = [row[1] / max2_emma for row in text2_emma.most_common(N)]
# plt.plot(range(N), [1 / (1 + i) for i in range(N)], c="k")
# # 왜 +1 을 했다고???????????????? -> 0부터 시작해서 1로 시작하려고
# plt.plot(range(N), freq1_emma, c="r")
# plt.plot(range(N), freq2_emma, c="b")
# print(list(zip(text1_emma.vocab().most_common(N), text2_emma.most_common(N)))[:5])
# plt.show()

# ! 최빈도 = 그 다음빈도x2 / 이 법칙이 안 맞으면 텍스트 처리가 어디서 된 거라는 걸 추측할 수 있다.


# ! 형태소 단위 분석
raw_kolaw = kolaw.open(kolaw.fileids()[0]).read()
ma = Komoran()
text1_kolaw = Text(word_tokenize(raw_kolaw))  # * 띄어쓰기+구두점
text2_kolaw = Text(ma.morphs(raw_kolaw))  # * 형태소
text3_kolaw = Text(
    ma.pos(raw_kolaw)
)  # * 형태소 + 품사 / 같은 글자도 문법 역할별로 구분
# ! 어절 / 토큰 => /s(단어)/s , 한 덩이를 어절이라고 부르는데 우리말은 /s(형태소+형태소..)/s
# ! 한 어절 => 여러계의 형태소로 분리가 되는데, 그 비율이 약 0.600, 형태소+품사 = 0.673 이더라..~
# ! 1.2-1.6이 적당
# ! .N() — 전체 토큰 개수 (중복 포함)
# ! "토큰이 총 몇 개 있나" — 같은 단어가 여러 번 나오면 그때마다 다 셈

# ! .B() — 고유 단어 개수 (중복 제거)
# ! "서로 다른 단어가 몇 종류 있나" — 같은 단어는 한 번만 세요. (Bins의 약자)
# print(text1_kolaw.vocab().B(), text2_kolaw.vocab().B(), text3_kolaw.vocab().B())
# print(text1_kolaw.vocab().N(), text2_kolaw.vocab().N(), text3_kolaw.vocab().N())

N = 100
# Text.FreqDist() = vocab() => Counter => Dict.max() => Dict.Key
# FreqDist[Key=text1_emma.max()] / text1_emma.vocab() 의 value 가 가장 많은 키를 찾은 거임
max1_kolaw = text1_kolaw.vocab()[text1_kolaw.vocab().max()]
max2_kolaw = text2_kolaw.vocab()[text2_kolaw.vocab().max()]
max3_kolaw = text3_kolaw.vocab()[text3_kolaw.vocab().max()]
freq1_kolaw = [row[1] / max1_kolaw for row in text1_kolaw.vocab().most_common(N)]
# => Sorted => [(k1,v1), (k2, v2), ...] X N
freq2_kolaw = [row[1] / max2_kolaw for row in text2_kolaw.vocab().most_common(N)]
freq3_kolaw = [row[1] / max3_kolaw for row in text3_kolaw.vocab().most_common(N)]
# plt.plot(range(N), [1 / (1 + i) for i in range(N)], c="k")
# plt.plot(range(N), freq1_kolaw, c="r")
# plt.plot(range(N), freq2_kolaw, c="g")
# plt.plot(range(N), freq3_kolaw, c="b")
# print(
#     list(
#         zip(
#             text1_kolaw.vocab().most_common(N),
#             text2_kolaw.vocab().most_common(N),
#             text3_kolaw.vocab().most_common(N),
#         )
#     )[:5]
# )
# plt.show()
# [
#     # ! 여기서 "하" 는 문법 상관없이 하 라는 단어만 세서
# !   말하다 / 하지마 -> 이런 것도 다 센 것이고
# !   겉모습(글자)이 같으면 무조건 같은 걸로 취급해서 셈
#     ((".", 357), ("하", 472), (("의", "JKG"), 387)),
#     ((",", 101), ("의", 387), ((".", "SF"), 360)),
#     (("수", 87), (".", 360), (("에", "JKB"), 330)),
#     # ! 여기서 "하" 는 품사 단위로 다 분석해서 아마 다른 하는 뒤 순위에 있을 것
# !   같은 글자라도 문법적 역할이 다르면 다른 항목으로 분리해서 셈
#     (("①", 75), ("에", 330), (("하", "XSV"), 326)),
#     (("또는", 70), ("는", 287), (("ㄴ다", "EF"), 243)),
# ]


raw_kobill = [kobill.open(f).read() for f in kobill.fileids()]

concat_kobill = re.sub(r"\s+", " ", "/n".join(raw_kobill))

text_kobill = Text(ma.morphs(concat_kobill))
# print(text_kobill.vocab().N(), text_kobill.vocab().B())

# ! Zipf => 최빈도 = 그 다음빈도x2, 순위의 역순 = 빈도순
# !  => (고빈도) | (중빈도) | (저빈도)
# !    기능0, 중요x         대표성x, 중요x
# ! 보통 빈도수에 따라 중요도가 정비례하는데 자연어에서는 그게 해당이 안될 수도 있다
# ! 많이 나온 단어도 안 중요할 수 있다 / 거의 안 나온 단어도 안 중요할 수 있다
# ! 오히려 중간에 있는 단어들이 중요하다


# * 고빈도 날리기
threshold = 0.5
maxfreq = text1_emma.vocab().N()
token_list = []
# for row in text1_emma.vocab().most_common():  # 빈도순으로 나열됨
#     token, freq = row
#     threshold -= freq / maxfreq
#     token_list.append(token)
#     if threshold < 0:
#         break

# print(len(token_list)) # -> 41개정도가 50% 차지하고 있다는 것을 알 수 있다.


# * 저빈도 날리기
threshold = 0.2
maxfreq = text1_emma.vocab().N()
token_list = []
# for row in text1_emma.vocab().most_common()[::-1]:  # 빈도 역순으로 나열됨
#     token, freq = row
#     threshold -= freq / maxfreq
#     token_list.append(token)
#     if freq > 1:
#         break

# print(len(token_list)) # -> 3416개 정도가 쓸데없는 단어들


threshold = 0.5

maxfreq = text3_kolaw.vocab().N()
token_list = []
# for row in text3_kolaw.vocab().most_common():  # 빈도순
#     token, freq = row
#     threshold -= freq / maxfreq
#     token_list.append(token)
#     if threshold < 0:
#         break


maxfreq = text3_kolaw.vocab().N()
token_list2 = []
# for row in text3_kolaw.vocab().most_common()[::-1]:  # 빈도역순
#     token, freq = row
#     threshold -= freq / maxfreq
#     token_list2.append(token)
#     if threshold < 0:
#         break

# print(len(list(set(text3_kolaw.tokens) - set(token_list) - set(token_list2))[:100]))
# print(list(set(text3_kolaw.tokens) - set(token_list) - set(token_list2))[:100])
# 본 문 은 어 쩌 고 어 쩌 고 => (본, 문, 은, 어, ...) => tokenizer
# 본문은 어쩌고 어쩌고 => (본문은, 어쩌고, ...) => tokenizer


def fileids(pk=None, fk=None):
    newslist = []
    with sqlite3.connect("news.db") as con:
        cur = con.cursor()
        cur.execute("""
                    select pk from news
                    """)
        newslist.extend([row[0] for row in cur.fetchall()])

        return newslist


news = []

for pk in fileids():
    with sqlite3.connect("news.db") as con:
        cur = con.cursor()
        cur.execute(
            """select title, content
                        from news where pk = ?
                        """,
            [pk],
        )

        news.append(cur.fetchone())


# print(news)


total_news = "/n/n".join([re.sub(r"\s+", " ", content[1]) for content in news])
# print(len(re.split(r"/n/n", total_news)), len(fileids()))
total_tokens = []  # [(형태소, 품사), (형태소, 품사)...]
# for line in re.split(r"/n/n", total_news):  # 개별 news의 content
#     total_tokens.extend(ma.pos(line))  # pos => [(형태소, 품사), (형태소, 품사)...]
# total_tokens = FreqDist(total_tokens)
# print(total_tokens.B(), total_tokens.N()) # NLTK.TEXT 객체로 변환


N = 100
# Text.FreqDist() = vocab() => Counter => Dict.max() => Dict.Key
# FreqDist[Key=text1_emma.max()] / text1_emma.vocab() 의 value 가 가장 많은 키를 찾은 거임
# max_tokens = total_tokens[total_tokens.max()]

# freq1_tokens = [row[1] / max_tokens for row in total_tokens.most_common(N)]

# plt.plot(range(N), [1 / (1 + i) for i in range(N)], c="k")
# plt.plot(range(N), freq1_tokens, c="r")
# print(total_tokens.most_common(5))
# plt.show()

# * 고빈도 날리기
threshold = 0.5
# maxfreq = total_tokens.N()
token_list = []
# for row in total_tokens.most_common():  # 빈도순으로 나열됨
#     token, freq = row
#     threshold -= freq / maxfreq
#     token_list.append(token)
#     if threshold < 0:
#         break


# ! -> 고빈도 7% 정도가 50%를 차지한다
# print(len(token_list), total_tokens.B() - len(token_list), total_tokens.B())

# * 저빈도 날리기
threshold = 0.5
# maxfreq = total_tokens.N()
token_list2 = []
# for row in total_tokens.most_common()[::-1]:  # 빈도순으로 나열됨
#     token, freq = row
#     threshold -= freq / maxfreq
#     token_list2.append(token)
#     if threshold < 0:
#         break
# print(len(token_list2), total_tokens.B() - len(token_list2), total_tokens.B())
# print(total_tokens.most_common()[109 : 109 + 620 + 1])

# ! Zipf : 고빈도 + 저빈도 보다 < 중빈도가 더 중요하다
# ! 고빈도 : 전체 유니크한 토큰들 중 약 2% 내인데, 전체의 50% 를 차지함
# ! 저빈도 : 약 1~2번정도, 문서의 특징을 온전히 담기가 힘듦
# ! (수식)TF-IDF(변형) => Okapi => BM25(Agent Hybrid Search)

# * Heaps; 문서의 길이와 문서 내 유니크한 토큰들 사이에는 특별한 함수 모양의 상관관계(점진적으로 증가)
# * - 1. 문서가 충분히 크다면, 대부분의 어휘들이 토큰에 포함됨 -> 데이터가 충분히 커야함
# * - 2. 시간이 지남에 따라 기계가 모르는(토큰에 포함되지 X) 단어들이 계속 생김 -> Out Of Vocabulary(OOV)

# * 문서의 길이가 점진적으로 커져야 함 -> 유니크한 토큰들 추출
# heaps1 = [""]
# # [0:'']
# for line in sent_tokenize(gutenberg.open(gutenberg.fileids()[0]).read()):
#     # [line:sent1, sent2, sent3, ...]
#     heaps1.append(heaps1[-1] + "/n/n" + line)
#     # [1:'' + '/n/n' + sent1] => 1000 => unique token?
#     # [2:heaps1[1] + '/n/n' + sent2] => 2000


# heaps1_text = Text(pos_tag(word_tokenize(line)) for line in heaps1[:1000])
# print(heaps1_text)


# * 문서별
heaps1 = []
for corpus in gutenberg.fileids():
    heaps1.append(
        Text(pos_tag(word_tokenize(gutenberg.open(corpus).read().lower()))).vocab()
    )

heaps1_text = [FreqDist()]
for heaps in heaps1:
    heaps1_text.append(heaps1_text[-1] + heaps)

heaps_law = lambda n, k=70, b=0.6: k * n**b
# k = 10-100 b = 0.4-0.6
length = [ht.N() for ht in heaps1_text]
uniq = [ht.B() for ht in heaps1_text]
plt.plot(length, uniq, c="k")
plt.plot(length, list(map(heaps_law, uniq)), c="r")
plt.show()

####### FeatureExtraction #######
# 텍스트데이터 -> 자연어처리 -> Tokens(OOV) -> Vector -> Model
# Zipf, Heaps의 법칙//Tokenizer      Vectorize
