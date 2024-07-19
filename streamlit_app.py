import streamlit as st
import pandas as pd

from rag_llm import RAGLLM

hotel_star_number_to_str = ["All", "OneStar", "TwoStar", "ThreeStar", "FourStar", "FiveStar"]


# 숙박 데이터 로드 함수
def load_data():
    data = pd.read_csv("csvs/processed_hotel_info2.csv")
    return pd.DataFrame(data)


# 메인 함수
def main():
    st.title("숙박 추천 앱")
    st.write("원하는 조건을 선택하고 추천 숙소를 확인하세요.")

    # 데이터 로드
    df = load_data()
    countyName_city_mapping = df

    # 필터링 옵션
    st.sidebar.header("필터 옵션")
    selected_countyName = st.sidebar.selectbox("국가 이름", countyName_city_mapping['countyName'].unique())

    cities_string = countyName_city_mapping[countyName_city_mapping['countyName'] == selected_countyName]['cityName'].unique()[0]
    cities = cities_string.split(", ")

    # 선택된 국가에 따라 cityName 선택
    selected_city = st.sidebar.selectbox("도시 이름", cities)

    # HotelRating 필터링
    all_ratings = st.sidebar.checkbox("모든 HotelRating ")
    if all_ratings:
        hotel_rating = 0
    else:
        hotel_rating = st.sidebar.slider("HotelRating", 1, 5, 3)

    # 유저 추가 요구사항 입력
    additional_requirements = st.sidebar.text_area("")

    ai_recommanded_flag = False

    # 검색 버튼
    if st.sidebar.button("검색"):
        # 필터링
        filtered_df = df[
            (df['countyName'] == selected_countyName) &
            (df['cityName'] == selected_city)
        ]
        hotel_rating_str = hotel_star_number_to_str[hotel_rating]

        st.session_state['filtered_df'] = filtered_df

        ai_recommanded_flag = additional_requirements.strip()
        if additional_requirements.strip():
            rag_llm = RAGLLM()
            result, infos = rag_llm.query_to_llm(
                hotel_rating=hotel_rating_str,
                country_name=selected_countyName,
                city_name=selected_city,
                user_query=additional_requirements
            )

            st.session_state['result'] = result

            print("\n호텔 상세 정보:")
            print(result)
            for hotel_info in infos:
                print(f"호텔명: {hotel_info['HotelName']}")
                print(f"주소: {hotel_info['Address']}")
                print(f"등급: {hotel_info['HotelRating']} 성급")
                print(f"설명: {hotel_info['Description'][:200]}…")
                print("—")

            print("infos type: ", type(infos))
            print("infos[0] type: ", type(infos[0]))
            infos = pd.concat(infos, ignore_index=True)

            infos = infos[
                (infos['HotelRating'] == hotel_star_number_to_str[hotel_rating])
            ]

            st.session_state['filtered_df'] = infos


    # 이전 검색 결과가 있는 경우 이를 유지
    if 'filtered_df' in st.session_state:
        filtered_df = st.session_state['filtered_df']

        # 결과 출력
        st.subheader("조건에 맞는 숙소")
        if not filtered_df.empty:
            if ai_recommanded_flag:
                st.write("")
                st.subheader("⭐ AI 추천 숙소!")
                st.write(st.session_state['result'])

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
                height: 350px;
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
                            <h3>{filtered_df.iloc[row * max_cols + idx]['HotelName']}</h3>
                            <p><strong>countyName:</strong> {filtered_df.iloc[row * max_cols + idx]['countyName']}</p>
                            <p><strong>cityName:</strong> {filtered_df.iloc[row * max_cols + idx]['cityName']}</p>
                            <p><strong>HotelRating:</strong> {filtered_df.iloc[row * max_cols + idx]['HotelRating']}</p>
                            <p><strong>Address:</strong> {filtered_df.iloc[row * max_cols + idx]['Address']}</p>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)

            if num_extra_items > 0:
                cols = st.columns(num_extra_items)
                for idx in range(num_extra_items):
                    with cols[idx]:
                        card_html = f"""
                        <div class="card">
                            <h3>{filtered_df.iloc[num_full_rows * max_cols + idx]['HotelName']}</h3>
                            <p><strong>countyName:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['countyName']}</p>
                            <p><strong>cityName:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['cityName']}</p>
                            <p><strong>HotelRating:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['HotelRating']}</p>
                            <p><strong>Address:</strong> {filtered_df.iloc[num_full_rows * max_cols + idx]['Address']}</p>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.write("조건에 맞는 숙소가 없습니다.")

if __name__ == "__main__":
    main()
