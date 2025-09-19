class ForeignKeyNotExist(Exception):
    pass


class CouldNotCreateEntityException(Exception):
    pass


class EntityAlreadyExistException(Exception):
    pass


class EntityNotFoundException(Exception):
    pass


class NotCombinedTablesException(Exception):
    pass


class InvalidTableOrderException(Exception):
    pass
