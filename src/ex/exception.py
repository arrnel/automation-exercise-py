class UserNotFoundError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class BrandNotFoundError(Exception):
    pass


class CookieNotFoundError(Exception):
    pass


class ParseByJsonPathError(Exception):
    pass


class DeserializationError(Exception):
    pass


class IssueNotFoundError(RuntimeError):
    pass


class RemoteFileNotFoundError(RuntimeError):
    pass


class RemoteVideoNotFoundError(RuntimeError):
    pass


class SelenoidError(RuntimeError):
    pass
