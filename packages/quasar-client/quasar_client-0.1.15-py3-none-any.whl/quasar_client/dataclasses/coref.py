"""Dataclasses for coref."""
from typing import List, Optional

from pydantic import BaseModel


class CorefCluster(BaseModel):
    """A coref cluster."""

    start: int
    end: int


class CorefMeta(BaseModel):
    """Metadata for coref output."""

    text: str
    resolved_text: Optional[str] = None
    clusters: Optional[List[List[CorefCluster]]] = None
