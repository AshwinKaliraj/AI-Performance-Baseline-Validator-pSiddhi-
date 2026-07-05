from pydantic import BaseModel


class ValidationRequest(BaseModel):
    current_value:float


class ValidationResponse(BaseModel):
    current_value:float
    z_score:float
    risk_level:str
    validation_status:str
    message:str