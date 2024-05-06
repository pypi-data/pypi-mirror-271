from pydantic import BaseModel, Field
from winion.record_key import RecordKey
from winion.record_value import RecordValue
# from winion.record_headers import RecordHeaders

class Record(BaseModel):
    key: RecordKey = Field()
    value: RecordValue = Field()
    # headers: RecordHeaders = Field()
