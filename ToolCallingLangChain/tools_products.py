from langchain.tools import tool
from vectorstore import get_retriever

retriever = get_retriever(k=3)


@tool("search_products")
def search_products(query: str, topK: int = 3) -> str:
    """Search the product catalog using semantic similarity and return relevant product details."""
    k = max(1, min(int(topK), 5))

    docs = retriever.invoke(query)  # returns List[Document]
    if not docs:
        return "NO_MATCH"

    return "\n\n---\n\n".join(d.page_content for d in docs[:k])
