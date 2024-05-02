import argparse

from .operations import transfer
from .parsers import parse_json_file


def _execute_transfer_operation(args: argparse.Namespace) -> None:
    connections = parse_json_file(args.connections)
    source_connection = connections[args.source]
    source_object = args.source_object
    source_query = args.source_query
    target_connection = connections[args.target]
    target_object = args.target_object
    batch_size = args.batch_size
    transfer(
        source_connection=source_connection,
        source_object=source_object,
        source_query=source_query,
        destination_connection=target_connection,
        target_object=target_object,
        batch_size=batch_size,
    )


def main():
    parser = argparse.ArgumentParser(description="ByteBridge CLI")
    subparsers = parser.add_subparsers(dest="operation", title="Operations")
    transfer_parser = subparsers.add_parser("transfer", help="Transfer data operation")
    transfer_parser.add_argument(
        "--connections",
        required=True,
        help="Path the JSON with the connections definitions",
    )
    transfer_parser.add_argument(
        "--source",
        required=True,
        help="The source name defined in the connections",
    )
    transfer_parser.add_argument(
        "--source-query",
        required=False,
        help="The query to be used to extract data from the source.",
    )
    transfer_parser.add_argument(
        "--source-object",
        required=False,
        help="The object from the source (table name or filepath) used to extract data.",
    )
    transfer_parser.add_argument(
        "--target",
        required=True,
        help="The target name defined in the connections.",
    )
    transfer_parser.add_argument(
        "--target-object",
        required=True,
        help="The object to load data in the target (a table name or a filepath)",
    )
    transfer_parser.add_argument(
        "--batch-size",
        required=False,
        default=100,
        type=int,
        help="The size of batches used during the data transfer.",
    )
    args = parser.parse_args()

    if args.operation == "transfer":
        _execute_transfer_operation(args)


if __name__ == "__main__":
    main()
