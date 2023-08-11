class FinanceBotException(Exception):
    pass


class UserAlreadyExists(FinanceBotException):
    pass


class UserDoesNotExist(FinanceBotException):
    pass


class UserNameNotDefined(FinanceBotException):
    pass


class UnsupportedInput(FinanceBotException):
    pass


class CategoryDoesNotExist(FinanceBotException):
    pass


class CategoryAlreadyExist(FinanceBotException):
    pass


class EmailAlreadyExist(FinanceBotException):
    pass
