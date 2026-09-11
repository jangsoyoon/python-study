import sqlite3
import re
from config import HEADERS
from urllib.parse import parse_qsl
from requests.compat import urljoin
from requests.sessions import Session
import requests
from selenium.webdriver import Chrome
from math import log, exp

# 내 메일 데이터를 이용한 스팸 분류기 만들기
# 1. 메일함에서 정상메일 + 스팸메일 가져오기
# 2. 전처리 어떻게 할지 생각하기
# 3. 전처리 방법을 바꿔서 NB 알고리즘에 적용하기
# 4. 전체 합이 50이라고 가정할 때, 1-20% 정도(5-10개 정도)만 학습용으로 사용하고 나머지는 테스트용으로 사용하기
# 5. test 결과를 비율로 표현하기 (5/5 => 5개 중 5개 결과가 다 일치)
mail_list = []


def get_mails():
    session = Session()
    cookie = {
        "NAC": "3ZcOBMhfaDyIB",
        "NNB": "WLGKAFBRRWHWU",
        "ASID": "dc786be7000001a04e4f26da0000001b",
        "cto_bundle": "M5L3el9EUVo1MkpIeVBKVUlCMkVzRUZ2NU9KZkg2YTNCSjAlMkZPbDF5Vlk0V0lxbk9KandoSFlDZG0lMkJXMVQ1SDZtM0l3MGFheHJNSDIlMkZZMG5nbmk4YThaWnFpM0RoaTBtYlhRNmRwc1RQbldyMHMyJTJGbXFlOENBV0lTN1RlU2NwdkF1UFZLMld1cWM2VHdzc09vT3haY1NpM21FQSUzRCUzRA",
        "_fbp": "fb.1.1788020291446.196023914717156212",
        "page_uid": "jquPElqosNossNKV0rd-377034",
        "NACT": "1",
        "SRT30": "1788914817",
        "SRT5": "1788920719",
        "nid_inf": "-1146801076",
        "NID_AUT": "TgYPSaHnFohM5O4666jt61KunR4XUBXskBnb3EyJcmzHC9iNCrH+KpZ4RTmvSiBl",
        "NMUSER": "DUjcEYkwzKC-E6tL2i-hM1Dc7fw3JQMICfvr_nmLbafuOvtqYi9UbSiNYIbOow4l7JYxE3u9Ye2H1t8TGJR67X9aIiyE5HHXGJCrUmE5OLEZl-GPNaVBF6neXkW1RIq1tfCCTjJIJ1rTjNPaO2UnAwkSK_ubm0o9QO45uwCwU95cL5eWMCx94-GgAwHEzavu6tv2DVB6ZYeJIpZvd6WPbSsdydXR34O_GkB44cBCV8S9jCLBYqRb",
        "BUC": "SDSEy_1WRdrT-ehAJNrEiTOZcJjrexZhdWewVEAsTnA=",
        "NID_SES": "AAABtcra1pwD4I5avSxBCo7/8c6XFOIMUfHJm2w3sP42yg1xiIKyHjNwXMesYV208QAFpxB7raM/AVXoCln1cggC9na0I3o6NYnL9fPPp9+vZvQUSJuvtI3CUuVgLKTuZZL3aSgShKShX0rVy+J+M+Spj8cz5KgG4TaDgoVQAYOz4uEot8QWBYcOlxVDY8Fs8pZ/TtQwj6mHFObIFvESOpUggteyYAdXTGRm5+CfQY1H2BoR9L8AXSpiigpNy5G58IoWV4GAadGs2qlF/4Iz3cSaHbINpVWzdKTqhl4/M2A65Pl2q4IPfNPXpGYaT2WMMZzeLyPwjIigYcTEeJ5MayksC9dthJUtM8iXFPg5gim0Rnwyv0SYWQzhsPLup9HS9Xb2S59HmdF38YVLL8xt6NkUZyJ/VqUp0T71nji77jDMx9dMAhIuFcE7gDXSpMipXLoYVmbCE2NzEdmknQe+28eF1ZzBLYDdIr6P0NZwIMuK2E3XsvUYXLCEN9THcCmDryCF6Qs3IklPJQ3YpkXaTS86M3reU9jNmBmMxDeY/wxWztPNREOK5NchXzKdJaDC6+hfiTzuRc3dbETALbSk31A73gU=",
    }

    url = "https://mail.naver.com/json/list?folderSN=0&page=1&viewMode=time&previewMode=1&sortField=1&sortType=0&u=1026jsy"
    url, params = url.split("?")
    params = dict(parse_qsl(params))
    resp = session.request(
        url=url, params=params, method="POST", cookies=cookie, headers=HEADERS
    )

    for i in range(10):
        url = f"https://mail.naver.com/json/list?folderSN=0&page={i}&viewMode=time&previewMode=1&sortField=1&sortType=0&u=1026jsy"
        url, params = url.split("?")
        params = dict(parse_qsl(params))
        resp = session.request(
            url=url, params=params, method="POST", cookies=cookie, headers=HEADERS
        )
        # print(resp.json()["mailData"])
        for mail in resp.json()["mailData"]:
            subject = mail["subject"].strip()
            label = "스팸" if subject.startswith(("[광고]", "(광고)")) else "정상"
            mail_list.append((subject, label))

    return mail_list


get_mails()

spam_subjects = [s for s, label in mail_list if label == "스팸"][:5]
normal_subjects = [s for s, label in mail_list if label == "정상"][:5]

C = ["스팸", "정상"]
D = [(s, "스팸") for s in spam_subjects] + [(s, "정상") for s in normal_subjects]


def training(C, D):
    V = list(set([word for row in D for word in row[0].lower().split()]))
    N = len(D)

    prior = dict()
    condprob = dict()
    for c in C:
        Nc = len([row for row in D if row[1] == c])
        prior[c] = Nc / N

        textc = " ".join([row[0] for row in D if row[1] == c])
        Tct = dict()
        for t in V:
            Tct[t] = len([token for token in textc.lower().split() if token == t])

        for t in V:
            if t not in condprob:
                condprob[t] = dict()
            condprob[t][c] = (Tct[t] + 1) / sum(Tct[token] + 1 for token in Tct)

    return V, prior, condprob


def apply(C, V, prior, condprob, subject):
    words = [w for w in subject.lower().split() if w in V]  # 사전에 있는 단어만 사용

    score = dict()
    for c in C:
        score[c] = log(prior[c])
        for w in words:
            score[c] += log(condprob[w][c])

    return max(score, key=score.get), score


V, prior, condprob = training(C, D)

spam_all = [s for s, label in mail_list if label == "스팸"]
normal_all = [s for s, label in mail_list if label == "정상"]

spam_test = spam_all[5:]  # 처음 5개(학습용) 빼고 나머지
normal_test = normal_all[5:]  # 처음 5개(학습용) 빼고 나머지
test_D = [(s, "스팸") for s in spam_test] + [(s, "정상") for s in normal_test]

correct = 0
total = len(test_D)

for subject, true_label in test_D:
    predicted, score = apply(C, V, prior, condprob, subject)
    is_correct = predicted == true_label
    if is_correct:
        correct += 1
    print(
        f"[{'O' if is_correct else 'X'}] '{subject}' -> 예측:{predicted} / 실제:{true_label}"
    )

print()
print(f"{correct}/{total}")


# ! 성능이 그렇게 좋지 않으니 성능을 조금 더 높일 방법을 생각할 것
