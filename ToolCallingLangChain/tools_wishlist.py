import json
from threading import Lock

from langchain.tools import tool

_store: dict[str, list[str]] = {}
_lock = Lock()


@tool("save_to_wishlist")
def save_to_wishlist(username: str, productTitle: str) -> str:
    """Save a product title to a user's wishlist (in-memory)."""
    with _lock:
        _store.setdefault(username, []).append(productTitle)
    return f"Saved: {productTitle}"


@tool("get_wishlist")
def get_wishlist(username: str) -> str:
    """Get the user's wishlist (in-memory)."""
    with _lock:
        items = list(_store.get(username, []))
    return json.dumps(items, ensure_ascii=False)
