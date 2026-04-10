import math

def haversine(lon1, lat1, lon2, lat2):
    # 지구 반지름 (km)
    R = 6371.0
    
    # 라디안 변환
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # 차이
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # 하버사인 공식
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

# 입력 받기 (경도, 위도 순 / 공백 구분)
print("첫 번째 좌표 입력 (경도 위도):")
lon1, lat1 = map(float, input().split())

print("두 번째 좌표 입력 (경도 위도):")
lon2, lat2 = map(float, input().split())

distance = haversine(lon1, lat1, lon2, lat2)

print(f"두 좌표 간 거리: {distance:.3f} km")