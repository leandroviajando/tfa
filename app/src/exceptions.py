class ErrorBase(Exception):
    """Base error"""


class NoBalanceMovementsError(ErrorBase):
    """No balance movements"""


class ForecastAlreadyExistsError(ErrorBase):
    """Forecast already exists"""


class NoUserAccountError(ErrorBase):
    """No user account"""
