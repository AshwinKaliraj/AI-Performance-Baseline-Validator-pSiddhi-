from pydantic import BaseModel

class BaselineResponse(BaseModel):

    moving_average:float

    standard_deviation:float

    current_value:float

    z_score:float

    status:str