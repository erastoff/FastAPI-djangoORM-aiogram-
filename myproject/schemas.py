from datetime import datetime
from pydantic import BaseModel


class Schema(BaseModel):
    input_start: datetime
