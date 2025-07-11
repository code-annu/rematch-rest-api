class ResourceNotFoundError(Exception):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class InvalidUpdateError(Exception):
    def __init__(self, message: str = "Invalid update data"):
        super().__init__(message)
