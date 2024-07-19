import pandas as pd
import chromadb
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

# 결측치 처리 (예: 결측치를 빈 문자열로 대체)
df_selected['HotelFacilities'] = df_selected['HotelFacilities'].fillna('')
df_selected['Description'] = df_selected['Description'].fillna('')

# 전처리된 원본 데이터를 CSV 파일로 저장
df_selected.to_csv('processed_hotel_selected.csv', index=False)

# 나라별 도시 매핑 생성 (중복 제거)
country_city_mapping = df_selected.groupby('countyName')['cityName'].apply(lambda x: list(set(x))).to_dict()

# 나라별 도시 매핑을 CSV 파일로 저장
with open('country_city_mapping.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Country', 'Cities'])
    for country, cities in country_city_mapping.items():
        writer.writerow([country, ', '.join(cities)])

# Chroma 클라이언트 초기화 (기본 설정 사용)
client = chromadb.Client()

# Chroma 컬렉션 생성
collection = client.create_collection("hotel_vectors")

# Description 컬럼을 벡터화하고 Chroma에 추가
ids = []
embeddings = []
embedding_rows = []

for index, row in df_selected.iterrows():
    description = row['Description']
    vector = client.encode(description)  # Chroma의 인코딩 메소드를 사용하여 벡터화
    ids.append(str(index))
    embeddings.append(vector)
    embedding_rows.append([row['countyName'], row['cityName'], row['HotelName'], vector])

collection.add(ids=ids, embeddings=embeddings)

# 벡터 데이터를 CSV 파일로 저장
with open('hotel_vectors_reduced.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    header = ['countyName', 'cityName', 'HotelName'] + [f'vector_{i}' for i in range(len(embeddings[0]))]
    writer.writerow(header)
    for row in embedding_rows:
        writer.writerow([row[0], row[1], row[2]] + row[3])

# 데이터 저장 확인을 위한 검색 예제
query_vector = embeddings[0]  # 첫 번째 벡터를 예제로 사용
results = collection.query(query_embeddings=[query_vector], n_results=5)

print("Search Results:")
if 'ids' in results and 'distances' in results:
    for idx, (result_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
        print(f"Result {idx + 1}: ID = {result_id}, Distance = {distance}")
else:
    print("Results not found. Raw output:")
    print(results)

# 나라별 도시 매핑 출력
print("Country-City Mapping:")
for country, cities in country_city_mapping.items():
    print(f"{country}: {', '.join(cities)}")

# 데이터프레임의 첫 몇 줄 확인
print(df_selected.head())

# 데이터프레임 정보 확인
print(df_selected.info())

# 결측치 확인
print(df_selected.isnull().sum())
