from pydantic import BaseModel


class AnomalyRequest(BaseModel):
    current_value:float


class AnomalyResponse(BaseModel):
    current_value:float
    moving_average:float
    standard_deviation:float
    z_score:float
    status:str