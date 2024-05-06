from pydantic import BaseModel, Field

class RecordKey(BaseModel):
    value: bytes = Field()
