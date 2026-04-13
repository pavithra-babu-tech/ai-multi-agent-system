from langchain.memory import ConversationBufferMemory

# Individual memory
research_memory = ConversationBufferMemory(memory_key="chat_history")
summary_memory = ConversationBufferMemory(memory_key="chat_history")

from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings

embedding = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = FAISS.from_texts(["start"], embedding)

shared_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever()
)