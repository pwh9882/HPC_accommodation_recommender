import pandas as pd


def load_data(file_path):
    # You can also try other encodings like 'iso-8859-1'
    df = pd.read_csv(file_path, encoding='latin1')
    return df


def main():
    # 데이터 로드
    df = load_data(
        "/Users/woohyeok/development/LLM_bootcamp/day4/HPC_accommodation_recommender/hotels.csv")

    print(df.head())


if __name__ == "__main__":
    main()
