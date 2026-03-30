import pandas as pd

df1 = pd.read_csv("119 신고접수 현황/신고접수_2024.csv", encoding="utf-8")
df2 = pd.read_csv("119 신고접수 현황/신고접수_2024.csv", encoding="utf-8", dtype={"DCLR_DT": str})

print("기본:")
print(df1.head())

print("\n문자열 강제:")
print(df2.head())

print(df1["DCLR_DT"].iloc[0], type(df1["DCLR_DT"].iloc[0]))