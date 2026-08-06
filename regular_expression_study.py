import re

from numpy import _1D

# data = "Adjfsielk"
# re.match('A', data).span
# re.match('A'.data).start(), re.match('A', data_filter.end()
# rst = re.match('ABC', data)
# data[rst.start():rst.end()]


# re.search("A.+J", data)
# re.search("A.{1,}J", data)
# re.search("A.+J", data)
# print(re.search("A.*J", data))


score = """
김이박 101010-1234564
이박김 102030-2231214
박김이 202020-3033334
김김김 303030-4000334
"""

# for line in data.splitlines():
#     if len(line) > 1:
#         result = ""
#         l1, r1 = line.split(" ")
#         l2, r2 = r1.split("-")
#         if len(r2) == 6 or len(r2) == 7:
#             result += l2 + "-" + "*" * len(r2)
#         result = l1 + " " + result
#         print(result)


# result = re.search(r"([0-9]{6})\-\d{7}", data)
# print(result)
# # print(re.sub(r"([0-9]{6})\-\d{7}", r"\g<1>-*******", data))
# print(re.sub(r"(\d{6})-\d{7}", r"\g<1>-*******", data))
# # print(re.sub(r"\d{7}", "*" * 7, data))

# print("\t")    # 진짜 탭 문자로 해석됨 (커서가 탭만큼 이동)
# print(r"\t")   # 그냥 '\'와 't' 두 글자! 탭이 아니라 문자 그대로

# p = re.compile("Crow|Servo")
# m = p.match("CrowHello")
# print(m)


# print(re.search(r"Life", "Life is too short"))


# print(re.search("^Life", "Life is too short"))

# print(re.search("short$", "Life is too short"))
# # print(re.search("short$", "Life is too short, you need python"))
# print(re.match("short$", "Life is too short"))


# p = re.compile("(ABC)+")
# m = p.search("ABCABCABC OK?")
# print(m)
# print(m.group())

# p = re.compile("((ABC)+)")
# m = p.search("ABCABCABC OK?")

# print(m.group(1))


# # compile 패턴을 객체로 만들 수 있다.

# # 패턴 1: r"\bclass\b" (양쪽 다 "단어 경계")
# # 의미: class가 독립된 완전한 단어여야 함 (앞뒤로 다른 문자가 안 붙어야 함)
# p = re.compile(r"\bclass\b")
# # 패턴 2: r"\Bclass\b" (앞은 "경계 아님", 뒤는 "경계")
# # 의미: class 앞에는 문자가 붙어있고(단어 중간), 뒤는 독립적으로 끝나야 함 → "~class"로 끝나는 단어를 찾음
# p = re.compile(r"\Bclass\b")
# # 패턴 3: r"\Bclass\B" (양쪽 다 "경계 아님")
# # 의미: class 앞뒤 모두 다른 문자에 완전히 파묻혀 있어야 함
# p = re.compile(r"\Bclass\B")
# print(p.search("no class at all"))
# print(p.search("one subclass is"))
# print(p.search("the declassified algorithm"))


# p = re.compile(r"\w+\s+\d+[\-]\d+[\-]\d+")
# m = p.search("park 010-1234-1234")
# print(m)


# c = re.search(r"\w+\s+(\d+[\-]?)+", "park 010-1234-1234")
# print(c)


score = """
010-1234-1234
505802-01-200209
"""


# print(re.search(r"\d+\-+\d+\-+\d+", data))
# print(re.search(r"[0-9]+\-[0-9]+\-[0-9]+", data))
# print(re.findall(r"[0-9]+\-[0-9]+\-[0-9]+", data, re.MULTILINE))
# print(re.findall(r"^[0-9]{3}\-[0-9]{4}\-[0-9]{4}+", data, re.MULTILINE))
# print(re.findall(r"\d+\-\d+\-\d+", data))
# print(re.findall(r"^\d{2,3}\-\d{4}\-\d{4}+", data, re.MULTILINE))
print(re.findall(r"^\d{2,}.\d{2,}.\d{2,}+", score, re.MULTILINE))


# re.findall(r'^?:\+\d{1,2}\D)?\d{2,3}\D\d{3,4}.\d{4}', data, re.MULTILINE)
# ?: 캡쳐는 안하는데 (그룹: +82) 이 ?(있을수도 있고, 없을 수도 있고)


re.findall(r"^(?:\+\d{1,2}\D)?[0]?\d{1,2}\D\d{3,4}.\d{4}", score, re.MULTILINE)
re.findall(r"^(?:\+\d{1,2}\D[0])?\d{1,2}\D\d{3,4}.\d{4}", score, re.MULTILINE)


score = """
id1234@domain.com
id.-_1234@domain.co.kr
idididid@mail.naver.com
go123ogle@google.com
kakao@mail.kakao.com
ididid_@email.com
"""

# print(re.findall(r"[a-zA-Z0-9._-]{5,}@(?:[.]?[a-z]{2,}){2,}", data))
# print(re.findall(r"[a-zA-Z0-9._-]{5,}@(?:[a-z]{2,}[.]?){2,}", data))

# 안쪽 [a-z]{2,} → "한 단어 조각이 최소 2글자는 되어야 한다" (예: co, kr처럼 1글자 도메인은 배제)
# 바깥쪽 (...)＋{2,} → "단어.단어 형태가 최소 2조각(2번) 이상 있어야 한다" (예: naver 하나만으론 부족, naver.com처럼 최소 2조각은 있어야 진짜 도메인)

score = """
http://www.naver.com
https://naver.com/
ftp://ftp.naver.com
telnet://naver.com
https://new.naver.com/secton/100
"""


# print(
#     re.findall(
#         r"^https?://(?:[.]?[a-z0-9]{2,}){2,}(?:[/][a-z0-9]{3,})*", data, re.MULTILINE
#     )
# )

# p = re.compile(r"^(https?)://((?:[.]?[a-z0-9]{2,}){2,})((?:[/][a-z0-9]{3,})*)")
p = re.compile(r"^(https?)://((?:[.]?[a-z0-9]{2,}){2,})((?:[/][a-z0-9]{3,})*)")
# print(p.search("https://new.naver.com/section/100").groups())

score = "1S2D*3T"
# p = re.compile(r"((\d\w)[*]?[#]?){3,}")
# p = re.compile(r"((\d)(\w)[*]?[#]?){3,}")

p = re.compile(r"(\d+)([SDT])([*#]?)")
results = p.findall(score)
print(results)
sdt = {"S": 1, "D": 2, "T": 3}
answers = []


def cal(answers) -> int:
    for score, bonus, option in results:
        # 돌면서 해당 result 가 숫자인지, 숫자면 뒤에 하나 가져와서 계산
        # 글자면 패스
        # 특수문자면
        cal_score = int(score) ** sdt[bonus]
        print(cal_score)
        answers.append(cal_score)
        print(f"뭔지 모르겠어: {answers[-2:]}")
        if option == "*":
            answers[-2:] = [x * 2 for x in answers[-2:]]

            print(f"계산: {answers[-2:]}")

        elif option == "#":
            answers[-1] *= -1

    return sum(answers)


# print(cal(answers))


# patterns = [p_obj, p_obj, p_obj, p_obj]
# patterns[2].split(patterns[1].search(patterns[0].sub)).group(1)
