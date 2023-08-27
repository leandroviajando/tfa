class ErrorBase(Exception):
    """Base error"""


class NoBalanceMovementsError(ErrorBase):
    """No balance movements"""


class AlreadyExistsError(ErrorBase):
    """Already exists"""


class NotFoundError(ErrorBase):
    """Not found"""


class NoUserAccountError(ErrorBase):
    """No user account"""
