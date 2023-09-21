from pydantic import BaseModel, Field, validator

from datetime import datetime, timedelta


class QueryParams(BaseModel):
    symbol: str
    start_date: str = None

    @property
    def calculate_end_date(self):
        """
        Calculate the end_date as start_date plus 9 additional cycles
        (10 total cycles)
        """
        if not self.start_date:
            return datetime.today().strftime("%Y-%m-%d")

        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
        # * cycle_duration) # Adjust cycle duration as needed
        end_date = start_date + timedelta(days=10)
        return end_date.strftime("%Y-%m-%d")

    @validator("symbol", pre=True, always=True)
    def uppercase_symbol(cls, value):
        if value is not None:
            return value.upper()


class RequestModel(BaseModel):
    query_params: QueryParams = None
    trackingId: str = Field(..., description="Tracking ID is required.")
