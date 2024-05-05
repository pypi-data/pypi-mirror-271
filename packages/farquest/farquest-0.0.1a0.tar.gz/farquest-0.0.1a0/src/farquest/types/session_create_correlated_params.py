# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SessionCreateCorrelatedParams"]


class SessionCreateCorrelatedParams(TypedDict, total=False):
    path_correlated_id: Required[Annotated[str, PropertyInfo(alias="correlatedId")]]

    body_correlated_id: Required[Annotated[str, PropertyInfo(alias="correlatedId")]]
