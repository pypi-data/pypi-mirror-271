class UnsupportedConnectorError(Exception):
    """Raised when an unsupported connector is used."""

    def __init__(self, connector_type):
        message = f"The connector {connector_type} is not supported."
        super().__init__(message)
