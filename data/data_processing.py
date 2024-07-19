import pandas as pd
import csv

# 다양한 인코딩 형식을 시도해보기
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

for encoding in encodings:
    try:
        df = pd.read_csv('hotels.csv', encoding=encoding)
        print(f"Successfully read the file with {encoding} encoding")
        break
    except UnicodeDecodeError:
        print(f"Failed to read the file with {encoding} encoding")

# 컬럼 이름의 공백 제거
df.columns = df.columns.str.strip()

# 컬럼 이름을 확인한 후 필요한 컬럼을 선택
selected_columns = ['countyName', 'cityName', 'HotelName', 'HotelRating', 'Address', 'HotelFacilities', 'Description']
df_selected = df[selected_columns].copy()

# Description이 비어있는 행 제거
df_selected = df_selected[df_selected['Description'].str.strip() != '']

# 나라별로 100개씩 샘플링
df_sampled = df_selected.groupby('countyName').apply(lambda x: x.sample(n=min(100, len(x)), random_state=1)).reset_index(drop=True)

# 전처리된 원본 데이터를 CSV 파일로 저장
df_sampled.to_csv('data_preprocessing/processed_hotel_selected.csv', index=False)

# 나라별 도시 매핑 생성 (중복 제거)
country_city_mapping = df_sampled.groupby('countyName')['cityName'].apply(lambda x: list(set(x))).to_dict()

# 나라별 도시 매핑을 CSV 파일로 저장
with open('data_preprocessing/country_city_mapping.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Country', 'Cities'])
    for country, cities in country_city_mapping.items():
        writer.writerow([country, ', '.join(cities)])

# 나라별 도시 매핑 출력
print("Country-City Mapping:")
for country, cities in country_city_mapping.items():
    print(f"{country}: {', '.join(cities)}")

# 데이터프레임의 첫 몇 줄 확인
print(df_sampled.head())

# 데이터프레임 정보 확인
print(df_sampled.info())

# 결측치 확인
print(df_sampled.isnull().sum())
