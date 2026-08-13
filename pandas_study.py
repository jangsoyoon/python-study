import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 시스템에 설치된 한글 폰트 경로 지정
plt.rcParams["font.family"] = "AppleGothic"  # macOS 기본 한글 폰트
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지
# df = pd.DataFrame()
# df["month"] = ["2026-" + str(x).zfill(2) for x in range(1, 13)]  ## 월(month)
# df["temperature"] = [
#     -2.4,
#     2.7,
#     9,
#     14.2,
#     17.1,
#     22.8,
#     28.1,
#     25.9,
#     22.6,
#     15.6,
#     8.2,
#     0.6,
# ]  ## 평균기온

# month = df["month"]
# temperature = df["temperature"]
# xtick_position = list(range(len(month)))

# fig = plt.figure(figsize=(12, 5))
# fig.set_facecolor("white")
# ax = fig.add_subplot()


# ax.plot(
#     xtick_position,
#     temperature,
#     color="#FFB7CE",
#     linestyle="--",
#     linewidth=2,
#     marker="*",
#     markersize=15,
#     markeredgecolor="#89CFF0",
#     markeredgewidth=1,
# )

# plt.xticks(
#     xtick_position, month, rotation=45, color="#FCEF91", fontweight="bold"
# )  # 위치+라벨 직접 지정
# plt.title(
#     "The Average Monthly Temperature", fontsize=20, color="#E0FFEF", fontweight="bold"
# )
# plt.tight_layout()
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(
    "./서울특별시 서대문구_도시공원 이용자수 현황_20201130.csv", encoding="cp949"
)
df["이용자수(명)"] = df["이용자수(명)"].astype(str).str.replace(",", "").astype(int)

month = df["월"]
users = df["이용자수(명)"]
xtick_position = list(range(len(month)))

fig, ax = plt.subplots(figsize=(10, 5))
fig.set_facecolor("white")
ax.set_facecolor("white")

# 1. 배경 이미지를 먼저 깔기
park_img = mpimg.imread("park.png")
ax.imshow(
    park_img,
    extent=[-0.5, len(month) - 0.5, 0, max(users) * 1.15],
    aspect="auto",
    alpha=0.15,  # 투명도 (낮을수록 흐릿함)
    zorder=0,  # 맨 뒤에 깔리도록
)

# 2. 막대 그래프를 그 위에 그리기
ax.bar(xtick_position, users, color="#639922", width=0.6, zorder=2)

# 3. 막대 위 숫자 라벨
for x, y in zip(xtick_position, users):
    ax.text(
        x,
        y + max(users) * 0.01,
        f"{y:,}",
        ha="center",
        fontsize=9,
        color="#3b6d11",
        zorder=3,
    )

plt.xticks(xtick_position, month, rotation=45)
plt.title("서대문구 도시공원 이용자수 (2020)", fontsize=16)
plt.ylabel("이용자수(명)")
ax.yaxis.set_major_formatter(lambda v, pos: f"{int(v/1000)}k")
ax.grid(axis="y", color="#e1e0d9", linewidth=0.8, zorder=1)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
