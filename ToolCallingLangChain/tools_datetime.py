from datetime import datetime
from zoneinfo import ZoneInfo

from langchain.tools import tool


@tool("getCurrentLocalTime")
def get_current_local_time() -> str:
    """Get current date-time in server/user default timezone (Asia/Kolkata here)."""
    return datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()


@tool("getCurrentTime")
def get_current_time(timeZone: str) -> str:
    """Get current time in the specified IANA timezone, e.g. Europe/London."""
    return datetime.now(ZoneInfo(timeZone)).strftime("%I:%M %p")
