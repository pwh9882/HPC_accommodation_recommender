from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

embedding_model = AzureOpenAIEmbeddings(
    model="text-embedding-3-small"
)
