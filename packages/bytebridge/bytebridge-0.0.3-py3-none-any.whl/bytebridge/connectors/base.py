from abc import ABC, abstractmethod
from typing import Iterator, List, Optional


class Connector(ABC):
    @abstractmethod
    def extract(
        self,
        *,
        source_object: Optional[str],
        source_query: Optional[str],
        batch_size: int,
    ):
        pass

    @abstractmethod
    def load(
        self,
        *,
        batch_iterator: Optional[Iterator[List[dict]]],
        target_object: str,
    ):
        pass
