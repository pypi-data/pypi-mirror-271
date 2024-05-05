# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
    Union,
)

from pydantic import (
    Field,
)
from pydantic.functional_validators import (
    field_validator,
)
from pydantic.types import SecretStr

from .__base import BaseUpdatableModel
from .__types import CustomUrl, FileUrl


class BaseConn(BaseUpdatableModel):
    type: str = "base"


class FlConn(BaseConn):
    type: Literal["file"] = "file"
    sys: str
    pointer: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    pwd: Optional[SecretStr] = None
    path: str
    options: Annotated[dict[str, Any], Field(default_factory=dict)]

    @classmethod
    def from_url(
        cls,
        url: Union[FileUrl, str],
    ) -> "FlConn":
        if isinstance(url, str):
            url = FileUrl(url=url)
        elif not isinstance(url, FileUrl):
            raise ValueError("A url value must be string or `FileUrl` object")
        return cls(
            sys=url.scheme,
            pointer=url.host,
            port=url.port,
            user=url.username,
            pwd=url.password,
            path=url.path,
            options=dict(url.query_params()),
        )


class DbConn(BaseConn):
    """Database Connection Model

    Example:
        *   {
                "type": "db",
                "driver": "sqlite",
            }
    """

    type: Literal["db"] = "db"
    driver: str
    host: str
    port: int
    user: str
    pwd: SecretStr
    db: str
    options: Annotated[dict[str, Any], Field(default_factory=dict)]

    @classmethod
    def from_url(
        cls,
        url: Union[CustomUrl, str],
    ) -> "DbConn":
        if isinstance(url, str):
            url = CustomUrl(url=url)
        elif not isinstance(url, CustomUrl):
            raise ValueError("A url value must be string or `CustomUrl` object")
        return cls(
            driver=url.scheme,
            host=url.host,
            port=url.port,
            user=url.username,
            pwd=url.password,
            db=url.path,
            options=dict(url.query_params()),
        )

    @field_validator("db")
    def check_db_name(cls, v: str) -> str:
        return v.lstrip("/").split("/")[0]
