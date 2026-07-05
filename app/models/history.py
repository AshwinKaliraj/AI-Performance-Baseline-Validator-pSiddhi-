from pydantic import BaseModel


class HistoryRequest(BaseModel):
    response_time:float


class HistoryResponse(BaseModel):
    message:str