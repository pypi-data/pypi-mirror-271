# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import quest_complete_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)

__all__ = ["QuestsResource", "AsyncQuestsResource"]


class QuestsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QuestsResourceWithRawResponse:
        return QuestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestsResourceWithStreamingResponse:
        return QuestsResourceWithStreamingResponse(self)

    def complete(
        self,
        *,
        correlation_id: str,
        quest_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Complete a quest

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/quest/complete",
            body=maybe_transform(
                {
                    "correlation_id": correlation_id,
                    "quest_id": quest_id,
                },
                quest_complete_params.QuestCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncQuestsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQuestsResourceWithRawResponse:
        return AsyncQuestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestsResourceWithStreamingResponse:
        return AsyncQuestsResourceWithStreamingResponse(self)

    async def complete(
        self,
        *,
        correlation_id: str,
        quest_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Complete a quest

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/quest/complete",
            body=await async_maybe_transform(
                {
                    "correlation_id": correlation_id,
                    "quest_id": quest_id,
                },
                quest_complete_params.QuestCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class QuestsResourceWithRawResponse:
    def __init__(self, quests: QuestsResource) -> None:
        self._quests = quests

        self.complete = to_raw_response_wrapper(
            quests.complete,
        )


class AsyncQuestsResourceWithRawResponse:
    def __init__(self, quests: AsyncQuestsResource) -> None:
        self._quests = quests

        self.complete = async_to_raw_response_wrapper(
            quests.complete,
        )


class QuestsResourceWithStreamingResponse:
    def __init__(self, quests: QuestsResource) -> None:
        self._quests = quests

        self.complete = to_streamed_response_wrapper(
            quests.complete,
        )


class AsyncQuestsResourceWithStreamingResponse:
    def __init__(self, quests: AsyncQuestsResource) -> None:
        self._quests = quests

        self.complete = async_to_streamed_response_wrapper(
            quests.complete,
        )
