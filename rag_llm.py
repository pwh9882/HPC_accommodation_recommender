from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import pandas as pd
import os

# 환경 변수 로드
load_dotenv()


class RAGLLM:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RAGLLM, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.df = None
        self.vector_db = None
        self.llm = None
        self.load_vector_db()
        self.load_data("csvs/processed_hotel_info2.csv")
        self.initialize_llm()

    def load_vector_db(self):
        embeddings = AzureOpenAIEmbeddings(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        )
        self.vector_db = Chroma(persist_directory="./vector_db",
                                embedding_function=embeddings)

    def initialize_llm(self):
        self.llm = AzureChatOpenAI(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

    def load_data(self, file_path):
        self.df = pd.read_csv(file_path, names=['countyCode', 'countyName', 'cityCode', 'cityName', 'HotelCode',
                                                'HotelName', 'HotelRating', 'Address', 'Attractions',
                                                'Description', 'FaxNumber', 'HotelFacilities', 'Map',
                                                'PhoneNumber', 'PinCode', 'HotelWebsiteUrl'])

    def get_hotel_info(self, hotel_code):
        # print(hotel_code)
        return self.df[self.df['HotelCode'] == hotel_code]

    def search_with_metadata_filter(self, query, metadata_filters):
        # where = {key: value for key, value in metadata_filters.items()}

        retriever = self.vector_db.as_retriever(
            search_type="similarity",
            # search_kwargs={"k": 4, "filter": where}
        )

        qa_chain = RetrievalQA.from_chain_type(
            self.llm, retriever=retriever, return_source_documents=True
        )

        return qa_chain.invoke({"query": query})

    def query_to_llm(self, user_query, country_name="All", city_name="All", hotel_rating="All"):
        metadata_filters = {}
        if country_name:
            metadata_filters["countyName"] = country_name
        if city_name:
            metadata_filters["cityName"] = city_name
        if hotel_rating:
            metadata_filters["HotelRating"] = hotel_rating

        # llm_answer = self.search_with_metadata_filter(
        #     f"language: korean, user_query: {user_query}\n ", metadata_filters)
        try:
            llm_answer = self.search_with_metadata_filter(
                f"output language: korean, country_name: {country_name}, city_name: {city_name}, hotel_rating: {hotel_rating} user_query: {user_query}\n ", metadata_filters)
            print("\n추천 호텔:")
            print(llm_answer['result'])

            if 'source_documents' in llm_answer and llm_answer['source_documents']:
                infos = [self.get_hotel_info(doc.metadata['HotelCode'])
                         for doc in llm_answer['source_documents']]
                # print("호텔 정보를 찾았습니다.", infos)
                return llm_answer['result'], infos

            else:
                print("검색 결과가 없습니다.")
                return "검색 결과가 없습니다.", []
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            print("시스템 관리자에게 문의하세요.")
            return "검색 결과가 없습니다.", []


if __name__ == "__main__":
    rag_llm = RAGLLM()
    result, infos = rag_llm.query_to_llm(
        user_query="wifi",
        country_name="South Korea",
        city_name="New York",
        hotel_rating="TwoStar",
    )
    print("\n호텔 상세 정보:")
    print(result)
    for hotel_info in infos:
        print(f"호텔명: {hotel_info['HotelName']}")
        print(f"주소: {hotel_info['Address']}")
        print(f"등급: {hotel_info['HotelRating']} 성급")
        print(f"설명: {hotel_info['Description'][:200]}…")
        print("—")
