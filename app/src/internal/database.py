from databases import Database

from src.internal.config import settings

database = Database(settings.SQLALCHEMY_DATABASE_URI)
