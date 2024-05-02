import logging
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.engine import ScalarResult, TupleResult
from sqlmodel import Session, SQLModel
from sqlmodel.sql import expression

from .errors import DatabaseExceptionFactory

logger = logging.getLogger(__name__)


class DatabaseOperator:
    def __init__(self, session: Session):
        self.__session = session

    def all(self, statement: expression.Select | expression.SelectOfScalar) -> Any:
        return self.__session.exec(statement).all()

    def first(self, statement: expression.Select | expression.SelectOfScalar) -> Any:
        return self.__session.exec(statement).first()

    def exec(self, statement: expression.Select | expression.SelectOfScalar) -> TupleResult | ScalarResult:
        result = self.__session.exec(statement)
        self.__session.commit()

        return result

    def create(self, model: type(SQLModel)) -> type(SQLModel):
        try:
            self.__session.add(model)
            self.__session.commit()
            self.__session.refresh(model)

            return model
        except Exception as e:
            DatabaseExceptionFactory.handle(e)

    def update(self, model: type(SQLModel)) -> type(SQLModel):
        try:
            if hasattr(model, 'updated_at'):
                model.updated_at = datetime.now(tz=timezone.utc)

            self.__session.add(model)
            self.__session.commit()
            self.__session.refresh(model)

            return model
        except Exception as e:
            DatabaseExceptionFactory.handle(e)

    def update_many(self, models: list[type(SQLModel)]) -> list[type(SQLModel)]:
        try:
            for model in models:
                self.__session.add(model)

            self.__session.commit()

            for model in models:
                self.__session.refresh(model)

            return models
        except Exception as e:
            DatabaseExceptionFactory.handle(e)

    def delete(self, model: type(SQLModel)) -> type(SQLModel):
        try:
            self.__session.delete(model)
            self.__session.commit()

            return model
        except Exception as e:
            DatabaseExceptionFactory.handle(e)

    def delete_many(self, models: list[type(SQLModel)]) -> list[type(SQLModel)]:
        try:
            for model in models:
                self.__session.delete(model)

            self.__session.commit()

            return models
        except Exception as e:
            DatabaseExceptionFactory.handle(e)
