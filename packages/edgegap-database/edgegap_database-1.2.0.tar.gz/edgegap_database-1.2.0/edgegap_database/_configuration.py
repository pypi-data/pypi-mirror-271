import logging

from pydantic import BaseModel, Field, PostgresDsn

from ._model import SQLiteDsn

logger = logging.getLogger(__name__)


class DatabaseConfiguration(BaseModel):
    uri: SQLiteDsn | PostgresDsn = Field(..., description='The URI of the database')
    application: str = Field(..., description='The Name of the Application for the DB connection')
    args: dict = Field(default=None, description='Extra Arguments for the DB connection')
