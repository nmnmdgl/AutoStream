# agent/rag.py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def setup_vectorstore():
    loader = TextLoader("data/pricing.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

    vectordb = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="chroma_db"
    )

    return vectordb

def query_rag(vectordb, question):
    docs = vectordb.similarity_search(question, k=3)
    print(f"[DEBUG] query_rag: Retrieved {len(docs)} documents")
    if docs:
        for i, doc in enumerate(docs):
            print(f"[DEBUG] Doc {i}: {doc.page_content[:150]}...")
        return docs[0].page_content
    else:
        print("[DEBUG] query_rag: No documents found")
        return "Sorry, I couldn't find pricing information on that."
