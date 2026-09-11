from heapq import merge
from string import punctuation
from unittest import result

from nltk.corpus import stopwords, gutenberg
from nltk.text import Text
from nltk.tokenize import word_tokenize
from konlpy.tag import Komoran, Kkma
from konlpy.corpus import kolaw
import re

# 불용어를 제거해야한다.
# print(stopwords.open("english").read())  # 대부분 대명사, be 동사, 접속사, 전치사...
eng_stop = stopwords.open("english").read()
emma = gutenberg.open("austen-emma.txt").read()
text1 = Text(word_tokenize(emma.lower()))
text2 = Text([t for t in word_tokenize(emma.lower()) if t not in eng_stop])
text3 = Text(
    [
        t
        for t in word_tokenize(emma.lower())
        if t not in eng_stop and t not in punctuation
    ]
)

# * Normalization = 일괄 소문자 치환
# print(text1.vocab().B(), text1.vocab().N())

# * 일괄 소문자 치환 + 불용어
# print(text2.vocab().B(), text2.vocab().N())

# * 일괄 소문자 치환 + 불용어 + 기호
# print(text3.vocab().B(), text3.vocab().N())

# * text1 보다 text2, 3이 기계가 이해하기에 훨씬 용이

s = "to be or not to be"
# print([t for t in word_tokenize(s) if t not in eng_stop])
# 이게 핵심 문장인데 관용구처럼 보거나 해야하는 것들을 날려버린다 -> 의미 전달을 못할 수도 있다 -> 상황에 따라 잘 써야한다.

s = "어머님 은 짜장면 이 싫다 고 하셨어 ."
kor_stop = "은이고"
# print([t for t in word_tokenize(s) if t not in kor_stop and t not in punctuation])
# -> ['어머님', '짜장면', '싫다', '하셨어']


s = "어머님은 짜장면이 싫다고 하셨어."
ma = Komoran()
[
    (t[0] + ("다" if t[1][0] == "V" else ""), t[1], ma.tagset[t[1]])
    for t in ma.pos(s)
    if t[1][0] not in ["J", "E"] and t[0] not in punctuation
]


law = kolaw.open(kolaw.fileids()[0]).read()

text1 = Text(word_tokenize(law))
text2 = Text(ma.morphs(law))
text3 = Text([t[0] for t in ma.pos(law) if t[1][0] == "N"])
# print(text1.vocab().B(), text1.vocab().N())
# print(text2.vocab().B(), text2.vocab().N())
# print(text3.vocab().B(), text3.vocab().N())

# print(text1) # <Text: 대한민국헌법 유구한 역사와 전통에 빛나는 우리 대한국민은 3·1운동으로...>
# print(text3) # <Text: 대한민국 헌법 역사 전통 우리 국민 운동 건립...>

s = "너 완전 밤티다. 나 지금 아바라 먹고싶어"

# print([(t[0], ma.tagset[t[1]]) for t in ma.pos(s)])
# print(ma.nouns(s))

#! 텍스트 데이터 => Encoding(카테고리형 데이터 -> 수치형 데이터) => Normalization => Vectorize
#!                          -------- => 어떤 게 있느냐? => NLP + 언어학
#!                          [Tokenization] => Feature Extraction / Feature Selection[불용어]


# 메일 가져와서 스팸인지 아닌지 구별하기
stopwords = ["씨발", "씨이발"]

s = "야이 씨발 씨이발 씨1발"
cleaned = []
for t in s.split():
    if t in stopwords:
        cleaned.append("*" * len(t))
    else:
        cleaned.append(t)

# print(" ".join(cleaned))

corpus = """
시발 시발 시발 시발 시발
씨발 씨발
시1발 씨2발 씨이발 시1발 씨2발 씨이발 시1발 씨2발 씨이발 씨!#$!@$!@#$!@#$!@#$!@#$!@#$!@#$!@#발
씨발아
"""


def preprocessing(d):
    # {'토 큰': 빈도}
    tokens = {}
    for token in d.split():
        token = " #".join(token) + " </w>"
        if token not in tokens:
            tokens[token] = 0
        tokens[token] += 1
    return tokens


def merge_vocab(be, vo):
    tokens = {}
    for k, v in vo.items():
        new_key = re.sub(re.escape(be), be.replace("#", "").replace(" ", ""), k)
        tokens[new_key] = v

    return tokens


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
# print(tokens)
history = list()
for i in range(10):
    pairs = get_stats(vocab)
    best = max(pairs, key=pairs.get)
    history.append(best)
    vocab = merge_vocab(best, vocab)


# print(vocab)

start = []
end = []
# print(list(set([k for t in vocab for k in t.split()])))
for t in list(set([k for t in vocab for k in t.split()])):
    # print(re.search(r'</w>$', t))
    if re.search(r"</w>$", t):
        end.append(t)
    elif re.search(r"^[^#]", t):
        start.append(t)

patterns = []
for s in start:
    for e in end:
        e = re.sub(r"</w>", "", e)
        patterns.append(re.compile(f"^{s}.*{e}$"))

# print(patterns)
s = "야이 씨발 씨이발 씨1발 씨21342314~@$!#$@!$발 씨발아"
cleaned = []
# print(patterns)
for t in s.split():
    # print(t)
    result = []
    for p in patterns:
        if p.search(t):
            result.append("*" * len(t))
            break
    if len(result) == 0:
        cleaned.append(t)
    else:
        cleaned.append(result[0])
# print(" ".join(cleaned))

# * 초중종
# * 가 => ㄱ ㅏ ' '
# * 음절 = 초+중+종
# * Trigem(삼보)
# * 1 (_ _초성 _) (_ _ 128~
# * _ _ _) (_ _종성 _)
# * ㄱ-ㅎ => 2^5 = 32
# * ㅏ-ㅣ => < 32
# * 조합형, 완성형, 확장완성형(CP949/ANSI), 유니코드(UTF8;3bytes)
# *       -------------------------- 문자테이블 0:가,1:나,...
# * 초중종 순서대로
# 자음: [chr(ord('ㄱ')+i) for i in range(30)]
# 모음: [chr(ord('ㅏ')+i) for i in range(21)]
# 종성: [chr(ord('가')+i) for i in range(28)]
# 중성: [chr(ord('가')+i*28) for i in range(21)]
# 초성: [chr(ord('가')+i*28*21) for i in range(19)]


def str2jamo(s):
    result = list()
    for c in s:
        if re.search("[가-힣]", c) != None:
            # ord(c='가') - ord('가') = 0
            base = ord(c) - ord("가")
            cho, jung = divmod(base, 28 * 21)
            jung, jong = divmod(jung, 28)
            # result.append(str(cho) + "|")
            # result.append(str(jung) + "|")
            # result.append(str(jong))
            result.append(cholist[cho])
            result.append(junglist[jung])
            result.append(jonglist[jong])
        else:
            result.append(c)

    return "".join(result)


# print(str2jamo("힣"), str2jamo("ABcd21길"))
# print([chr(ord("ㄱ") + i) for i in range(30)])
# print([chr(ord("가") + i * 28) for i in range(21)])
# print([chr(ord("ㄱ") + i) for i in range(30)])
# # ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# print([chr(ord("가") + i * 28 * 21) for i in range(19)])
# ['가', '까', '나', '다', '따', '라', '마', '바', '빠', '사', '싸', '아', '자', '짜', '차', '카', '타', '파', '하']
cholist = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]
cholist[18]
"ㅎ"
# print([chr(ord("가") + i * 28) for i in range(21)])
# ['가', '개', '갸', '걔', '거', '게', '겨', '계', '고', '과', '괘', '괴', '교', '구', '궈', '궤', '귀', '규', '그', '긔', '기']
# print([chr(ord("ㅏ") + i) for i in range(21)])
# ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
junglist = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]
# print([chr(ord("ㄱ") + i) for i in range(30)])
# ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# print([chr(ord("가") + i) for i in range(28)])
# ['가', '각', '갂', '갃', '간', '갅', '갆', '갇', '갈', '갉', '갊', '갋', '갌', '갍', '갎', '갏', '감', '갑', '값', '갓', '갔', '강', '갖', '갗', '갘', '같', '갚', '갛']
jonglist = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]
# print(cholist[18], junglist[20], jonglist[27])
# ('ㅎ', 'ㅣ', 'ㅎ')


def jamo2str(s1, s2, s3):
    cho, jung, jong = s1, s2, s3
    cho_no = cholist.index(cho)  # 0:'ㄱ', 1: 'ㄲ',..
    jung_no = junglist.index(jung)  # 0:'ㅏ', 1: 'ㅣ',..
    jong_no = jonglist.index(jong)  # 0:' ', 1: 'ㄱ',..

    c = cho_no * 28 * 21
    c += jung_no * 28
    c += jong_no

    return chr(ord("가") + c)


# print(jamo2str("ㄱ", "ㅏ", "ㄴ"), jamo2str("ㅎ", "ㅣ", "ㅎ"))


# 같은 길이의 두 문자열 or 벡터일 때, 얼마나 같은지를 측정하는 방법
def hammingDistance(s1, s2):
    if len(s1) != len(s2):
        return sum([1 if c1 == c2 else 0 for c1, c2 in zip(s1, s2)])


# print(hammingDistance(str2jamo("고려대학교"), str2jamo("골렫대학교")))


def lev(a, b):
    if len(b) == 0:
        return len(a)
    if len(a) == 0:
        return len(b)

    if a[0] == b[0]:
        return lev(a[1:], b[1:])
    else:
        return 1 + min([lev(a[1:], b), lev(a, b[1:]), lev(a[1:], b[1:])])


# print(lev("고려대학교", "집에가고싶다"[::-1]))

print(hammingDistance("안녕", "아녕"))
print(lev("안녕", "아령"))

univ_list = ["고려대", "연세대", "서강대", "동덕여대"]
key = "골려대"

print(key in univ_list)

for univ in univ_list:
    print(univ, hammingDistance(univ, key), lev(univ, key))
    if lev(univ, key) < 0.2:
        print(">>", univ)
