from pydantic import BaseModel
from datetime import datetime

class ProjectBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {
            # How to get time in milliseconds ref:https://currentmillis.com/#methods
            datetime: lambda v: int(round(v.timestamp() * 1000)),
        }
        exclude_none = True