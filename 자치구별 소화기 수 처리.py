import pandas as pd
import geopandas as gpd


# =========================================
# 비상소화장치위치 -> 자치구 별 소화장치 개수 변환
# =========================================

# 1. load

df = pd.read_excel("서울시 비상소화장치 위치정보.xlsx")


# 2. 데이터 정제

# 2-1. 삭제여부 확인
deleted_count = (df['삭제여부'] == 'Y').sum()
print(f"삭제여부 Y 개수: {deleted_count}")
print(df[df['삭제여부'] == 'Y'].head())

# 2-2. 고장(52203~52207) 제거
df_clean = df[~df['사용구분'].between(52203, 52207)]

# 2-3. 삭제 데이터 제거
df_clean = df_clean[df_clean['삭제여부'] != 'Y']

# 결과 확인
print(f"원본 개수: {len(df)}")
print(f"정제 후 개수: {len(df_clean)}")


# 3. 공간 데이터 변환


# GeoDataFrame 생성 (ITRF2000 / EPSG:5186)
gdf = gpd.GeoDataFrame(
    df_clean,
    geometry=gpd.points_from_xy(df_clean['X좌표'], df_clean['Y좌표']),
    crs="EPSG:5186"
)

# WGS84로 변환 (GeoJSON 맞추기)
gdf = gdf.to_crs(epsg=4326)


# 4. 서울시 자치구 GeoJSON 불러오기

seoul = gpd.read_file("seoul.geojson")
seoul = seoul.to_crs(epsg=4326)

# 컬럼 확인 (구 이름 컬럼 찾기)
print(seoul.columns)


# 5. 공간 조인 (자치구 매핑)

joined = gpd.sjoin(gdf, seoul, how="left", predicate="within")


# 6. 자치구별 소화기 개수 집계

result = joined.groupby('SIG_KOR_NM').size().reset_index(name='소화기개수')


# 7. 결과 저장

result.to_csv("output/자치구별 소화기 개수.csv", index=False, encoding='utf-8-sig')

print(result)