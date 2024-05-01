### cntrlai/__init__.py
import os
from cntrlai.logger import span, create_span, capture_rag

endpoint = (
    os.environ.get("CONTROLAI_ENDPOINT") or "https://app.controlai.org"
)
api_key = os.environ.get("CONTROLAI_API_KEY")

__all__ = ("endpoint", "api_key", "span", "create_span")
