# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["OrganizationCreateParams"]


class OrganizationCreateParams(TypedDict, total=False):
    auth_redirect_url: Required[Annotated[str, PropertyInfo(alias="authRedirectUrl")]]

    callback_url: Required[Annotated[str, PropertyInfo(alias="callbackUrl")]]

    name: Required[str]
