from dotenv import load_dotenv

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

loader = TextLoader("product_details.txt", encoding="utf8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = splitter.split_documents(docs)

vectordb = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory="chroma_db"
)

retriever = vectordb.as_retriever(search_kwargs={"k": 3})

@tool("search_products")
def search_products(query: str) -> str:
    """Search the product catalog using semantic similarity and return the most relevant product details."""
    results = retriever.invoke(query)  # retriever returns Documents
    if not results:
        return "NO_MATCH"

    return "\n\n---\n\n".join([d.page_content for d in results])

model = ChatOpenAI(model="gpt-4o")

agent = create_agent(
    model=model,
    tools=[search_products],
    system_prompt="""
You are a product assistant for a small catalog.

Rules:
- For any product question, call the tool `search_products` first.
- Answer ONLY using the tool output.
- If tool output is NO_MATCH, say: "I don't know."
"""
)

question = "wireless earbuds under $50"
result = agent.invoke({"messages": [{"role": "user", "content": question}]})

print(result["messages"][-1].content)
