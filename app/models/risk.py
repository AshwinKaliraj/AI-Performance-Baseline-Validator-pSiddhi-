from pydantic import BaseModel


class RiskRequest(BaseModel):
    current_value:float


class RiskResponse(BaseModel):
    current_value:float
    moving_average:float
    standard_deviation:float
    z_score:float
    risk_score:int
    risk_level:str