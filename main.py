import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from plt_style import set_korean 

# 한글 설정
set_korean()

# 2. 행정동 GeoJSON 로드 (좌표계: WGS84)
hjd_gdf = gpd.read_file('polygon/서울시_행정동.geojson')
hjd_gdf = hjd_gdf.to_crs("EPSG:4326")

# 3. 119 신고 데이터 로드 (UTF-8-SIG 적용)
df_dispatch = pd.read_csv('119 신고접수 현황/신고접수_2024.csv', encoding='utf-8-sig')

# 컬럼명 정리
df_dispatch.columns = df_dispatch.columns.str.strip().str.upper()

# [핵심 수정] DAMG_RGN 좌표가 있는 '실제 사건'만 필터링
# DAMG_RGN_LOT(경도, X), DAMG_RGN_LAT(위도, Y) 기준
df_clean = df_dispatch.dropna(subset=['DAMG_RGN_LOT', 'DAMG_RGN_LAT']).copy()

# [필터링] 위경도 범위 내 정상 데이터만 유지. "서울시로 한정"이 아닌 "한국 한정"임. (rough하게 처리)
valid_lon = (df_clean['DAMG_RGN_LOT'] > 124) & (df_clean['DAMG_RGN_LOT'] < 132)
valid_lat = (df_clean['DAMG_RGN_LAT'] > 33) & (df_clean['DAMG_RGN_LAT'] < 40)
df_final = df_clean[valid_lon & valid_lat].copy()

print(f"원본 데이터: {len(df_dispatch)}건")
print(f"실제 사건(DAMG_RGN 존재): {len(df_final)}건")

# 4. GeoDataFrame 변환 (실제 피해 지점 DAMG_RGN 기준)
gdf_actual = gpd.GeoDataFrame(
    df_final, 
    geometry=gpd.points_from_xy(df_final['DAMG_RGN_LOT'], df_final['DAMG_RGN_LAT']),
    crs="EPSG:4326")

# 5. 시각화
fig, ax = plt.subplots(1, 1, figsize=(15, 12))

# 하위 레이어: 서울 행정동 경계
hjd_gdf.plot(ax=ax, color='#f2f2f2', edgecolor='black', linewidth=0.6, zorder=1)

# 상위 레이어: 실제 피해 지점 (aspect='equal'로 왜곡 방지)
if not gdf_actual.empty:
    gdf_actual.plot(ax=ax, color='blue', markersize=1, alpha=0.1, zorder=2, label='실제 사고 지점', aspect='equal')
else:
    print("필터링 후 남은 데이터가 없습니다.")

# 전체 분포를 보기 위해 xlim, ylim 설정은 생략
ax.set_title("2024년 119 실제 사고 발생 분포 (DAMG_RGN 기준)", fontsize=18)
ax.set_axis_off()
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()


#################################
###### 가공 후 csv 저장 ###########
#################################
# --- 기존 5번 시각화 코드 이후에 추가 ---

# 6. 행정동 별 사고 건수 집계 (Spatial Join)
# hjd_gdf에서 동 이름 컬럼명을 확인하세요 (보통 'ADM_DR_NM' 혹은 'HJD_NM') => adm_nm
dong_name_col = 'adm_nm' 

# 최적화: 필요한 컬럼(geometry, 이름)만 추출하여 공간 결합 수행
hjd_subset = hjd_gdf[[dong_name_col, 'geometry']]
joined_gdf = gpd.sjoin(gdf_actual, hjd_subset, predicate='within', how='inner')

# 행정동별 그룹화 및 카운트
dong_counts = joined_gdf.groupby(dong_name_col).size().reset_index(name='사고건수')
dong_counts = dong_counts.sort_values(by='사고건수', ascending=False)

# 7. 안전센터 별 출동횟수 집계
# PLCSCN_CNTR_NM 열을 기준으로 중복 횟수 산출
center_counts = df_final['PLCSCN_CNTR_NM'].value_counts().reset_index()
center_counts.columns = ['안전센터명', '출동횟수']

# 8. CSV 파일 저장 (UTF-8-SIG 적용으로 한글 깨짐 방지)
dong_counts.to_csv('output/행정동_별_사고_건수.csv', index=False, encoding='utf-8-sig')
center_counts.to_csv('output/안전센터_별_출동횟수.csv', index=False, encoding='utf-8-sig')

# 결과 출력 확인
print("\n" + "="*30)
print("✅ 데이터 집계 완료 및 CSV 저장 성공!")
print(f"1. 행정동 별 사고 건수: {len(dong_counts)}개 동 기록")
print(f"2. 안전센터 별 출동횟수: {len(center_counts)}개 센터 기록")
print("="*30)

# 맛보기 출력
print("\n[행정동별 사고건수 상위 5개]")
print(dong_counts.head())
print("\n[안전센터별 출동횟수 상위 5개]")
print(center_counts.head())