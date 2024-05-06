from typing import Optional
from winion.record_key import RecordKey
from winion.record_value import RecordValue
from winion.record_headers import RecordHeaders


class ProducerMixin(object):
    def produce(
        self,
        topic: str,
        key: Optional[RecordKey],
        __value__: RecordValue,
        __headers__: RecordHeaders,
    ):
        print(f"ProducerMixin#produce topic={topic}, key={key}")
