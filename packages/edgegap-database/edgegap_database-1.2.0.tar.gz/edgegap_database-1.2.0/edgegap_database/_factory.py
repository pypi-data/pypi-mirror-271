import logging

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl

from ._configuration import DatabaseConfiguration
from ._model import SQLiteDsn

logger = logging.getLogger(__name__)


class DatabaseConfigurationFactory:
    @staticmethod
    def __parse(conf: DatabaseConfiguration) -> DatabaseConfiguration:
        if conf.application is None:
            conf.application = 'DefaultApplicationName'

        if not isinstance(conf.args, dict):
            conf.args = {}

        conf.args.update({
            'application_name': conf.application,
            'options': '-c timezone=utc',
        })

        return conf

    def from_uri(self, uri: str | MultiHostUrl | PostgresDsn | SQLiteDsn, name: str) -> DatabaseConfiguration:
        configuration = DatabaseConfiguration(uri=str(uri), application=name)

        return self.__parse(configuration)
