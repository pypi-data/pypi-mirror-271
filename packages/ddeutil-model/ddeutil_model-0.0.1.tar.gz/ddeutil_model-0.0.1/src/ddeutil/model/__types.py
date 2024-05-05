# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from typing import Annotated

from pydantic.networks import UrlConstraints
from pydantic_core import Url

CustomUrl = Annotated[
    Url,
    UrlConstraints(
        host_required=True,
        default_port=1234,
    ),
]

FileUrl = Annotated[
    Url, UrlConstraints(default_host="localhost", default_port="22")
]
