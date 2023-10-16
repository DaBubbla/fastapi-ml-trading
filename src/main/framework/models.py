from pydantic import (
    BaseModel, Field, validator
)
from typing import List, Optional
from datetime import datetime, timedelta


class QueryParams(BaseModel):
    symbol: str

    @validator("symbol", pre=True, always=True)
    def uppercase_symbol(cls, value):
        if value is not None:
            return value.upper()


class RequestModel(BaseModel):
    query_params: QueryParams = None
    trackingId: str = Field(..., description="Tracking ID is required.")


class DemarkData(BaseModel):
    timestamp: str = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: int = None
    setup: float = None
    countdown: float = None

class PredicteCloseSummary(BaseModel):
    min_close: float = 0.0
    mean_close: float = 0.0
    max_close: float = 0.0
    mean_squared_error: float = 0.0
    r_squared: float = 0.0

class ResponseModel(BaseModel):
    predicted_close_rf: PredicteCloseSummary = None
    predicted_close_lr: PredicteCloseSummary = None
    predicted_xgb: PredicteCloseSummary = None
    demark_data: List[DemarkData] = []
