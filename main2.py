import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("seoul.geojson")

ax = gdf.plot(figsize=(8, 8), edgecolor="black", alpha=0.5)

# 자치구 이름 표시
for idx, row in gdf.iterrows():
    plt.text(
        row.geometry.centroid.x,
        row.geometry.centroid.y,
        row["SIG_KOR_NM"],
        fontsize=8,
        ha='center'
    )

import folium

gdf = gpd.read_file("seoul.geojson").to_crs(epsg=4326)

m = folium.Map(location=[37.55, 126.98], zoom_start=11)

# 폴리곤 + 이름
folium.GeoJson(
    gdf,
    tooltip=folium.GeoJsonTooltip(fields=["SIG_KOR_NM"])
).add_to(m)

m.save("map.html")