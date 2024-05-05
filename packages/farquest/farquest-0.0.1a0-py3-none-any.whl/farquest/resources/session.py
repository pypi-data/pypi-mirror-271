# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import session_create_correlated_params
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

__all__ = ["SessionResource", "AsyncSessionResource"]


class SessionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionResourceWithRawResponse:
        return SessionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionResourceWithStreamingResponse:
        return SessionResourceWithStreamingResponse(self)

    def create_correlated(
        self,
        *,
        path_correlated_id: str,
        body_correlated_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a new session with a correlated ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_correlated_id:
            raise ValueError(f"Expected a non-empty value for `path_correlated_id` but received {path_correlated_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/session/{path_correlated_id}",
            body=maybe_transform(
                {"correlated_id": body_correlated_id}, session_create_correlated_params.SessionCreateCorrelatedParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSessionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionResourceWithRawResponse:
        return AsyncSessionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionResourceWithStreamingResponse:
        return AsyncSessionResourceWithStreamingResponse(self)

    async def create_correlated(
        self,
        *,
        path_correlated_id: str,
        body_correlated_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a new session with a correlated ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_correlated_id:
            raise ValueError(f"Expected a non-empty value for `path_correlated_id` but received {path_correlated_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/session/{path_correlated_id}",
            body=await async_maybe_transform(
                {"correlated_id": body_correlated_id}, session_create_correlated_params.SessionCreateCorrelatedParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SessionResourceWithRawResponse:
    def __init__(self, session: SessionResource) -> None:
        self._session = session

        self.create_correlated = to_raw_response_wrapper(
            session.create_correlated,
        )


class AsyncSessionResourceWithRawResponse:
    def __init__(self, session: AsyncSessionResource) -> None:
        self._session = session

        self.create_correlated = async_to_raw_response_wrapper(
            session.create_correlated,
        )


class SessionResourceWithStreamingResponse:
    def __init__(self, session: SessionResource) -> None:
        self._session = session

        self.create_correlated = to_streamed_response_wrapper(
            session.create_correlated,
        )


class AsyncSessionResourceWithStreamingResponse:
    def __init__(self, session: AsyncSessionResource) -> None:
        self._session = session

        self.create_correlated = async_to_streamed_response_wrapper(
            session.create_correlated,
        )
