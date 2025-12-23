from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = Path("chroma_db")


def get_vectorstore(txt_path: str = "product_details.txt") -> Chroma:
    load_dotenv()
    embeddings = OpenAIEmbeddings()

    if PERSIST_DIR.exists() and any(PERSIST_DIR.iterdir()):
        return Chroma(persist_directory=str(PERSIST_DIR), embedding_function=embeddings)

    docs = TextLoader(txt_path, encoding="utf8").load()
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

    db = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR),
    )
    return db


def get_retriever(k: int = 3):
    """Get retriever from vectorstore"""
    db = get_vectorstore()
    return db.as_retriever(search_kwargs={"k": k})