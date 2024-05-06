from pydantic import BaseModel, Field

class RecordValue(BaseModel):
    value: bytes = Field()
