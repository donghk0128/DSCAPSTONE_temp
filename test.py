import pandas as pd

# 확인할 연도 범위
years = range(2021, 2025)

for year in years:
    file_name = f"화재사고 구조출동 현황/화재사고_{year}.csv"
    try:
        df = pd.read_csv(file_name)
        rows, cols = df.shape
        print(f"{year}.csv: {rows}개")
    except FileNotFoundError:
        print(f"{file_name}: 파일 없음")
print(cols)
    