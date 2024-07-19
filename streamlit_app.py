import streamlit as st
import pandas as pd


# 데이터 로드 함수
def load_data():
    # 예시 데이터 프레임
    data = {
        '숙소명': [f'호텔 {chr(65 + i)}' for i in range(20)],
        '나라': ['한국'] * 20,
        '도시': ['서울'] * 20,
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
    df = load_data()

    # 필터링 옵션
    st.sidebar.header("필터 옵션")
    country = st.sidebar.selectbox("나라", df['나라'].unique())
    cities = df[df['나라'] == country]['도시'].unique()
    city = st.sidebar.selectbox("도시", cities)
    hotel_rating = st.sidebar.slider("호텔 등급", 1, 5, 3)

    # 유저 추가 요구사항 입력
    additional_requirements = st.sidebar.text_area("")

    # 필터링
    filtered_df = df[
        (df['나라'] == country) &
        (df['도시'] == city) &
        (df['호텔 등급'] >= hotel_rating) &
        (df['편의시설'].str.contains(additional_requirements, case=False))
        ]

    # 결과 출력
    st.subheader("추천 숙소")
    if not filtered_df.empty:
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
