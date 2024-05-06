from typing import List
from winion.record import Record


class ConsumerGroupMixin(object):
    def consume(
        self,
        topic: str,
        records: List[Record],
    ):
        print(f"ProducerMixin#consume topic={topic}")
