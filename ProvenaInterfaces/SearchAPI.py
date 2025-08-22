from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from enum import Enum

try:
    from ProvenaInterfaces.SharedTypes import StatusResponse
except:
    from .SharedTypes import StatusResponse


class SearchResultType(str, Enum):
    DATASET = "DATASET"
    REGISTRY_ITEM = "REGISTRY_ITEM"


class QueryResult(BaseModel):
    id: str
    score: float


class MixedQueryResult(QueryResult):
    type: SearchResultType


class QueryResults(StatusResponse):
    results: Optional[List[QueryResult]] = None
    warnings: Optional[List[str]] = None


class MixedQueryResults(StatusResponse):
    results: Optional[List[MixedQueryResult]] = None
    warnings: Optional[List[str]] = None
