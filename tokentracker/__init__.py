"""TokenTracker — drop-in LLM cost tracker. Change one import line, see where your money goes."""

__version__ = "0.1.0"

from tokentracker.client import OpenAI, AsyncOpenAI
from tokentracker.db import get_db
from tokentracker.query import summary, recent, cost_by_model, cost_by_day

__all__ = [
    "OpenAI",
    "AsyncOpenAI",
    "get_db",
    "summary",
    "recent",
    "cost_by_model",
    "cost_by_day",
]
