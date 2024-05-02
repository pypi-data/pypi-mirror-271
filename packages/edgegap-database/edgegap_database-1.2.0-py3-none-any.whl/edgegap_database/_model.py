from typing import Annotated

from pydantic.networks import UrlConstraints
from pydantic_core import Url

SQLiteDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=[
            'sqlite',
        ],
        default_port=3306,
    ),
]
