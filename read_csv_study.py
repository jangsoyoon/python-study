import pandas as pd

df = pd.read_csv(
    "./csv/서울특별시 서대문구_도시공원 이용자수 현황_20201130.csv", encoding="cp949"
)

# print(df.columns.str.strip())

df_top10 = df[["월", "이용자수(명)"]].head(10)

print(df_top10)

new_row = pd.DataFrame([{"월": "2020-11월", "이용자수(명)": "23,900"}])

df_result = pd.concat([df_top10, new_row], ignore_index=True)

print(df_result)
