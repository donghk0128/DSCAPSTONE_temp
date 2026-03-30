import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from plt_style import set_korean 

# 1. 한글 설정
set_korean()

# 2. 행정동 GeoJSON 로드 (좌표계: WGS84)
hjd_gdf = gpd.read_file('서울시_행정동.geojson')
print(hjd_gdf)