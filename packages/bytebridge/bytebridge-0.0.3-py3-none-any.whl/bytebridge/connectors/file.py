import csv
import itertools
from typing import Iterator, List

import pyarrow
from pyarrow import parquet

from .base import Connector


class ParquetConnector(Connector):
    def __init__(self, *, connection_parameters: dict) -> None:
        self._connection_parameters = connection_parameters

    def extract(
        self,
        *,
        source_object: str,
        source_query: str,
        batch_size: int,
    ) -> Iterator[List[dict]]:
        parquet_file = parquet.ParquetFile(source_object)
        for batch in parquet_file.iter_batches(batch_size=batch_size):
            yield batch.to_pylist()

    def load(
        self,
        *,
        target_object: str,
        batch_iterator: Iterator[dict],
    ):
        first_batch = next(batch_iterator)
        if first_batch:
            record_batch = pyarrow.RecordBatch.from_pylist(first_batch)
            with parquet.ParquetWriter(target_object, record_batch.schema) as writer:
                writer.write_batch(record_batch)
                for batch in batch_iterator:
                    writer.write_batch(batch=pyarrow.RecordBatch.from_pylist(batch))


class CsvConnector(Connector):
    def __init__(self, *, connection_parameters: dict) -> None:
        self._delimiter = connection_parameters.get("delimiter", ",")

    def extract(
        self,
        *,
        source_object: str,
        source_query: str,
        batch_size: int,
    ) -> Iterator[List[dict]]:
        with open(source_object) as source_file:
            csv_reader = csv.DictReader(source_file, delimiter=self._delimiter)
            while batch := tuple(itertools.islice(csv_reader, batch_size)):
                yield batch

    def load(
        self,
        *,
        target_object: str,
        batch_iterator: Iterator[dict],
    ):
        first_batch = next(batch_iterator)
        if first_batch:
            with open(target_object, "w") as target_file:
                csv_writer = csv.DictWriter(
                    target_file,
                    fieldnames=first_batch[0].keys(),
                    delimiter=self._delimiter,
                )
                csv_writer.writeheader()
                csv_writer.writerows(first_batch)
                for batch in batch_iterator:
                    csv_writer.writerows(batch)
