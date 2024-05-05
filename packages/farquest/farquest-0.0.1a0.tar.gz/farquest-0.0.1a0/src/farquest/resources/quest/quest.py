# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from .types import (
    TypesResource,
    AsyncTypesResource,
    TypesResourceWithRawResponse,
    AsyncTypesResourceWithRawResponse,
    TypesResourceWithStreamingResponse,
    AsyncTypesResourceWithStreamingResponse,
)
from ...types import quest_create_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .validation import (
    ValidationResource,
    AsyncValidationResource,
    ValidationResourceWithRawResponse,
    AsyncValidationResourceWithRawResponse,
    ValidationResourceWithStreamingResponse,
    AsyncValidationResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .completions import (
    CompletionsResource,
    AsyncCompletionsResource,
    CompletionsResourceWithRawResponse,
    AsyncCompletionsResourceWithRawResponse,
    CompletionsResourceWithStreamingResponse,
    AsyncCompletionsResourceWithStreamingResponse,
)
from ..._base_client import (
    make_request_options,
)

__all__ = ["QuestResource", "AsyncQuestResource"]


class QuestResource(SyncAPIResource):
    @cached_property
    def types(self) -> TypesResource:
        return TypesResource(self._client)

    @cached_property
    def completions(self) -> CompletionsResource:
        return CompletionsResource(self._client)

    @cached_property
    def validation(self) -> ValidationResource:
        return ValidationResource(self._client)

    @cached_property
    def with_raw_response(self) -> QuestResourceWithRawResponse:
        return QuestResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestResourceWithStreamingResponse:
        return QuestResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        description: str,
        ends_at: Union[str, datetime],
        image: str,
        name: str,
        organization_id: str,
        quest_type_id: str,
        starts_at: Union[str, datetime],
        validation_criteria: object,
        custom_callback_metadata: object | NotGiven = NOT_GIVEN,
        custom_metadata: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a new quest

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/quest/create",
            body=maybe_transform(
                {
                    "description": description,
                    "ends_at": ends_at,
                    "image": image,
                    "name": name,
                    "organization_id": organization_id,
                    "quest_type_id": quest_type_id,
                    "starts_at": starts_at,
                    "validation_criteria": validation_criteria,
                    "custom_callback_metadata": custom_callback_metadata,
                    "custom_metadata": custom_metadata,
                },
                quest_create_params.QuestCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get a quest by ID, optionally for a specific user by their ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/quest/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        filter: Literal["ACTIVE", "COMPLETE", "ALL", "NOT_STARTED"] | NotGiven = NOT_GIVEN,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get quests paginated, optionally with a filter

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not filter:
            raise ValueError(f"Expected a non-empty value for `filter` but received {filter!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/quest/list/{filter}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncQuestResource(AsyncAPIResource):
    @cached_property
    def types(self) -> AsyncTypesResource:
        return AsyncTypesResource(self._client)

    @cached_property
    def completions(self) -> AsyncCompletionsResource:
        return AsyncCompletionsResource(self._client)

    @cached_property
    def validation(self) -> AsyncValidationResource:
        return AsyncValidationResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncQuestResourceWithRawResponse:
        return AsyncQuestResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestResourceWithStreamingResponse:
        return AsyncQuestResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        description: str,
        ends_at: Union[str, datetime],
        image: str,
        name: str,
        organization_id: str,
        quest_type_id: str,
        starts_at: Union[str, datetime],
        validation_criteria: object,
        custom_callback_metadata: object | NotGiven = NOT_GIVEN,
        custom_metadata: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a new quest

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/quest/create",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "ends_at": ends_at,
                    "image": image,
                    "name": name,
                    "organization_id": organization_id,
                    "quest_type_id": quest_type_id,
                    "starts_at": starts_at,
                    "validation_criteria": validation_criteria,
                    "custom_callback_metadata": custom_callback_metadata,
                    "custom_metadata": custom_metadata,
                },
                quest_create_params.QuestCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get a quest by ID, optionally for a specific user by their ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/quest/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        filter: Literal["ACTIVE", "COMPLETE", "ALL", "NOT_STARTED"] | NotGiven = NOT_GIVEN,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get quests paginated, optionally with a filter

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not filter:
            raise ValueError(f"Expected a non-empty value for `filter` but received {filter!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/quest/list/{filter}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class QuestResourceWithRawResponse:
    def __init__(self, quest: QuestResource) -> None:
        self._quest = quest

        self.create = to_raw_response_wrapper(
            quest.create,
        )
        self.retrieve = to_raw_response_wrapper(
            quest.retrieve,
        )
        self.list = to_raw_response_wrapper(
            quest.list,
        )

    @cached_property
    def types(self) -> TypesResourceWithRawResponse:
        return TypesResourceWithRawResponse(self._quest.types)

    @cached_property
    def completions(self) -> CompletionsResourceWithRawResponse:
        return CompletionsResourceWithRawResponse(self._quest.completions)

    @cached_property
    def validation(self) -> ValidationResourceWithRawResponse:
        return ValidationResourceWithRawResponse(self._quest.validation)


class AsyncQuestResourceWithRawResponse:
    def __init__(self, quest: AsyncQuestResource) -> None:
        self._quest = quest

        self.create = async_to_raw_response_wrapper(
            quest.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            quest.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            quest.list,
        )

    @cached_property
    def types(self) -> AsyncTypesResourceWithRawResponse:
        return AsyncTypesResourceWithRawResponse(self._quest.types)

    @cached_property
    def completions(self) -> AsyncCompletionsResourceWithRawResponse:
        return AsyncCompletionsResourceWithRawResponse(self._quest.completions)

    @cached_property
    def validation(self) -> AsyncValidationResourceWithRawResponse:
        return AsyncValidationResourceWithRawResponse(self._quest.validation)


class QuestResourceWithStreamingResponse:
    def __init__(self, quest: QuestResource) -> None:
        self._quest = quest

        self.create = to_streamed_response_wrapper(
            quest.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            quest.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            quest.list,
        )

    @cached_property
    def types(self) -> TypesResourceWithStreamingResponse:
        return TypesResourceWithStreamingResponse(self._quest.types)

    @cached_property
    def completions(self) -> CompletionsResourceWithStreamingResponse:
        return CompletionsResourceWithStreamingResponse(self._quest.completions)

    @cached_property
    def validation(self) -> ValidationResourceWithStreamingResponse:
        return ValidationResourceWithStreamingResponse(self._quest.validation)


class AsyncQuestResourceWithStreamingResponse:
    def __init__(self, quest: AsyncQuestResource) -> None:
        self._quest = quest

        self.create = async_to_streamed_response_wrapper(
            quest.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            quest.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            quest.list,
        )

    @cached_property
    def types(self) -> AsyncTypesResourceWithStreamingResponse:
        return AsyncTypesResourceWithStreamingResponse(self._quest.types)

    @cached_property
    def completions(self) -> AsyncCompletionsResourceWithStreamingResponse:
        return AsyncCompletionsResourceWithStreamingResponse(self._quest.completions)

    @cached_property
    def validation(self) -> AsyncValidationResourceWithStreamingResponse:
        return AsyncValidationResourceWithStreamingResponse(self._quest.validation)
