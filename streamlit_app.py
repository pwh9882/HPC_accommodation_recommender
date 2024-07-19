import streamlit as st
import pandas as pd

# 국가-도시 매핑 데이터 로드 함수
def load_country_city_mapping():
    csv_file_path = 'country_city_mapping.csv'
    return pd.read_csv(csv_file_path)

# 숙박 데이터 로드 함수
def load_data():
    # 예시 데이터 프레임
    data = {
        '숙소명': [f'호텔 {chr(65 + i)}' for i in range(20)],
        '나라': ['Albania'] * 20,
        '도시': ['Albanien'] * 20,
        '호텔 등급': [5, 4, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 4, 3, 5, 4, 3, 5, 4, 3],
        '편의시설': ['Wi-Fi, 조식 포함', '주차 가능, 수영장', '반려동물 동반 가능', 'Wi-Fi, 무료 주차', 'Wi-Fi, 조식 포함',
                 '주차 가능, 수영장', '반려동물 동반 가능', 'Wi-Fi, 무료 주차', 'Wi-Fi, 조식 포함', '주차 가능, 수영장',
                 '반려동물 동반 가능', 'Wi-Fi, 무료 주차', 'Wi-Fi, 조식 포함', '주차 가능, 수영장', '반려동물 동반 가능',
                 'Wi-Fi, 무료 주차', 'Wi-Fi, 조식 포함', '주차 가능, 수영장', '반려동물 동반 가능', 'Wi-Fi, 무료 주차']
    }
    return pd.DataFrame(data)

# 메인 함수
def main():
    st.title("숙박 추천 앱")
    st.write("원하는 조건을 선택하고 추천 숙소를 확인하세요.")

    # 데이터 로드
    country_city_mapping = load_country_city_mapping()
    df = load_data()

    # 필터링 옵션
    st.sidebar.header("필터 옵션")
    selected_country = st.sidebar.selectbox("나라", country_city_mapping['Country'].unique())

    cities_string = country_city_mapping[country_city_mapping['Country'] == selected_country]['Cities'].unique()[0]
    cities = cities_string.split(", ")

    # 선택된 국가에 따라 도시 선택
    selected_city = st.sidebar.selectbox("도시", cities)

    hotel_rating = st.sidebar.slider("호텔 등급", 1, 5, 3)

    # 유저 추가 요구사항 입력
    additional_requirements = st.sidebar.text_area("")

    # 검색 버튼
    if st.sidebar.button("검색"):
        # 필터링
        filtered_df = df[
            (df['나라'] == selected_country) &
            (df['도시'] == selected_city) &
            (df['호텔 등급'] >= hotel_rating) &
            (df['편의시설'].str.contains(additional_requirements, case=False))
        ]
        st.session_state['filtered_df'] = filtered_df

    # 이전 검색 결과가 있는 경우 이를 유지
    if 'filtered_df' in st.session_state:
        filtered_df = st.session_state['filtered_df']

        ai_recommanded_flag = additional_requirements != ""

        # 결과 출력
        st.subheader("조건에 맞는 숙소")
        if not filtered_df.empty:
            if ai_recommanded_flag:
                st.write("")
                st.subheader("⭐ AI 추천 숙소!")
                st.write("추가된 글자 예시입니다.")

            num_rows = len(filtered_df)
            max_cols = 3
            num_full_rows = num_rows // max_cols
            num_extra_items = num_rows % max_cols

            card_style = """
            <style>
            .card {
                background-color: #f8f9fa;
                padding: 20px;
                margin: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 100%;
                height: 250px;
                overflow: hidden;
                flex-grow: 1;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }
            .container .card {
                margin: 5% 0;
            }
            @media (prefers-color-scheme:dark) {
            .card{
                background-color: #333;
                color : #fff;
            }
            }
            </style>
            """

            st.markdown(card_style, unsafe_allow_html=True)

            for row in range(num_full_rows):
                cols = st.columns(max_cols)
                for idx in range(max_cols):
                    with cols[idx]:
                        card_html = f"""
                        <div class="card">
                            <h3>{filtered_df.iloc[row * max_cols + idx]['숙소명']}</h3>
                            <p><strong>나라:</strong> {filtered_df.iloc[row * max_cols + idx]['나라']}</p>
                            <p><strong>도시:</strong> {filtered_df.iloc[row * max_cols + idx]['도시']}</p>
                            <p><strong>호텔 등급:</strong> {filtered_df.iloc[row * max_cols + idx]['호텔 등급']}성급</p>
                            <p><strong>편의시설:</strong> {filtered_df.iloc[row * max_cols + idx]['편의시설']}</p>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)

            if num_extra_items > 0:
                cols = st.columns(num_extra_items)
                for idx in range(num_extra_items):
                    with cols[idx]:
                        card_html = f"""
                        <div class="card">
                            <h3>{filtered_df.iloc[num_full_rows * max_cols + idx]['숙소명']}</h3>
                            <p><strong>나라:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['나라']}</p>
                            <p><strong>도시:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['도시']}</p>
                            <p><strong>호텔 등급:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['호텔 등급']}성급</p>
                            <p><strong>편의시설:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['편의시설']}</p>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.write("조건에 맞는 숙소가 없습니다.")

if __name__ == "__main__":
    main()
