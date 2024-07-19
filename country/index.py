import pandas as pd
import os

# 입력 CSV 파일 경로
input_file_path = 'hotels.csv'

# 출력 폴더 생성
output_dir = 'country_data'
os.makedirs(output_dir, exist_ok=True)

# 다양한 인코딩 형식을 시도해보기
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

# CSV 파일 읽기
df = None
for encoding in encodings:
    try:
        df = pd.read_csv(input_file_path, encoding=encoding)
        print(f"Successfully read the file with {encoding} encoding")
        break
    except UnicodeDecodeError:
        print(f"Failed to read the file with {encoding} encoding")
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        break

# 데이터가 제대로 로드되었는지 확인
if df is not None:
    # 컬럼 이름의 공백 제거
    df.columns = df.columns.str.strip()

    # 나라 목록
    countries = [
        "Albania", "Andorra", "Antigua", "Argentina", "Aruba", "Australia", "Austria",
        "Azerbaijan", "Bahamas", "Bahrain", "Barbados", "Belarus", "Belgium", "Bolivia",
        "Bosnia Herzegovina", "Botswana", "Brazil", "Brunei Darussalam", "Bulgaria",
        "Cambodia", "Cameroon", "Canada", "Chile", "China", "Colombia", "Cook Islands",
        "Costa Rica", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Dominican Republic",
        "Ecuador", "Egypt", "Estonia", "Ethiopia", "Fiji", "Finland", "France",
        "French Polynesia", "Germany", "Gibraltar", "Greece", "Grenada", "Guadeloupe",
        "Guam", "Guatemala", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia",
        "Ireland(Republic of)", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kenya",
        "Kuwait", "Laos", "Latvia", "Lebanon", "Libya", "Liechtenstein", "Lithuania",
        "Luxembourg", "Macau", "Malaysia", "Malta", "Mauritius", "Mexico", "Monaco",
        "Mongolia", "Morocco", "Myanmar", "Namibia", "Nepal", "Netherlands", "New Caledonia",
        "New Zealand", "Nigeria", "Northern Mariana Isl", "Norway", "Oman", "Palau",
        "Panama", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico",
        "Qatar", "Romania", "Russia", "Russian Federation", "Samoa", "San Marino",
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Singapore", "Slovakia",
        "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka", "St Kitts & Nevis",
        "St Lucia", "St Vincent & Grenadi", "Swaziland", "Sweden", "Switzerland", "Taiwan",
        "Tanzania", "Thailand", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey",
        "Turks & Caicos Islan", "Ukraine", "United Arab Emirates", "United Kingdom",
        "United States", "Uruguay", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (USA)",
        "Yemen Republic", "Zambia", "Zimbabwe"
    ]

    for country in countries:
        # 나라별로 100개씩 조정
        df_country = df[df['countyName'].str.contains(country, case=False, na=False)]
        df_country = df_country.head(100)

        # Description이 비어있는 것은 빼기
        df_country_filtered = df_country[df_country['Description'].notna() & df_country['Description'].str.strip().astype(bool)]

        # 나라별 CSV 파일로 저장
        output_file_path = os.path.join(output_dir, f'{country}.csv')
        df_country_filtered.to_csv(output_file_path, index=False)
        print(f"Data for '{country}' saved to '{output_file_path}'")

else:
    print("DataFrame not created. Please check the file path and encoding.")
