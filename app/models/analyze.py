from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    current_value:float


class AnalyzeResponse(BaseModel):
    baseline:dict
    anomaly:dict
    risk:dict
    validation:dict
    recommendation:dict