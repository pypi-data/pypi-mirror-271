from typing import Any, Dict, Optional, Type

from bytebridge.connectors.base import Connector
from bytebridge.connectors.database import (
    MsSqlConnector,
    MySqlConnector,
    PostgresConnector,
)
from bytebridge.connectors.file import CsvConnector, ParquetConnector
from bytebridge.exceptions import UnsupportedConnectorError


def _get_connector(connector_type: str) -> Type[Connector]:
    supported_connectors = {
        "postgresql": PostgresConnector,
        "mysql": MySqlConnector,
        "parquet": ParquetConnector,
        "mssql": MsSqlConnector,
        "csv": CsvConnector,
    }
    if connector_type not in supported_connectors:
        raise UnsupportedConnectorError(connector_type=connector_type)
    return supported_connectors[connector_type]


def transfer(
    *,
    source_query: Optional[str],
    source_object: Optional[str],
    source_connection: Dict[str, Any],
    batch_size: int,
    target_object: str,
    destination_connection: Dict[str, Any],
) -> None:
    if not source_query and not source_object:
        raise ValueError("Either 'source_query' or 'source_object' must be provided.")

    source_connector = _get_connector(source_connection["type"])(
        connection_parameters=source_connection.get("parameters"),
    )
    destination_connector = _get_connector(destination_connection["type"])(
        connection_parameters=destination_connection.get("parameters", {}),
    )
    batch_iterator = source_connector.extract(
        source_query=source_query,
        source_object=source_object,
        batch_size=batch_size,
    )
    destination_connector.load(
        batch_iterator=batch_iterator,
        target_object=target_object,
    )
