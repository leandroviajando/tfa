from src.internal.database import database


def get_db():
    yield database
