# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["QuestCreateParams"]


class QuestCreateParams(TypedDict, total=False):
    description: Required[str]

    ends_at: Required[Annotated[Union[str, datetime], PropertyInfo(alias="endsAt", format="iso8601")]]

    image: Required[str]

    name: Required[str]

    organization_id: Required[Annotated[str, PropertyInfo(alias="organizationId")]]

    quest_type_id: Required[Annotated[str, PropertyInfo(alias="questTypeId")]]

    starts_at: Required[Annotated[Union[str, datetime], PropertyInfo(alias="startsAt", format="iso8601")]]

    validation_criteria: Required[Annotated[object, PropertyInfo(alias="validationCriteria")]]

    custom_callback_metadata: Annotated[object, PropertyInfo(alias="customCallbackMetadata")]

    custom_metadata: Annotated[object, PropertyInfo(alias="customMetadata")]
