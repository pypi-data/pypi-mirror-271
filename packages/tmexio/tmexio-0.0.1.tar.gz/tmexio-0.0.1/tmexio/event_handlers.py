from __future__ import annotations

from abc import ABC
from collections.abc import Awaitable, Callable, Iterator
from typing import Any, cast
from warnings import warn

from pydantic import BaseModel, ValidationError
from socketio.exceptions import ConnectionRefusedError  # type: ignore[import-untyped]

from tmexio.exceptions import EventException
from tmexio.markers import Marker
from tmexio.packagers import CodedPackager, ErrorPackager
from tmexio.structures import ClientEvent
from tmexio.types import DataOrTuple, DataType


class BaseAsyncHandler:
    def __init__(
        self,
        async_callable: Callable[..., Awaitable[Any]],
        marker_destinations: list[tuple[Marker[Any], list[str]]],
    ) -> None:
        self.async_callable = async_callable
        self.marker_destinations = marker_destinations

    def build_markers(self, event: ClientEvent) -> Iterator[tuple[str, Any]]:
        for marker, parameter_names in self.marker_destinations:
            value = marker.extract(event)
            yield from ((name, value) for name in parameter_names)

    async def __call__(self, event: ClientEvent) -> DataOrTuple:
        raise NotImplementedError


class EventBodyException(EventException):
    def __init__(self, validation_error: ValidationError) -> None:
        super().__init__(code=422, ack_body=cast(DataType, validation_error.errors()))


class UndocumentedExceptionWarning(RuntimeWarning):
    def __init__(self, exception: EventException) -> None:
        super().__init__(f"Exception {exception} is not documented, but was raised")


class BaseAsyncHandlerWithArguments(BaseAsyncHandler, ABC):
    error_packager: ErrorPackager = ErrorPackager()

    zero_arguments_expected_error = EventException(422, "Event expects zero arguments")
    one_argument_expected_error = EventException(422, "Event expects one argument")

    def __init__(
        self,
        async_callable: Callable[..., Awaitable[Any]],
        marker_destinations: list[tuple[Marker[Any], list[str]]],
        body_model: type[BaseModel] | None,
        body_destinations: list[tuple[str, list[str]]],
        possible_exceptions: set[EventException],
    ) -> None:
        super().__init__(
            async_callable=async_callable,
            marker_destinations=marker_destinations,
        )
        self.body_model = body_model
        self.body_destinations = body_destinations
        self.possible_exceptions = possible_exceptions

    def parse_args(self, event: ClientEvent) -> Iterator[tuple[str, Any]]:
        if self.body_model is None:
            if len(event.args) != 0 and event.args[0] is not None:
                raise self.zero_arguments_expected_error
        else:
            if len(event.args) != 1:
                raise self.one_argument_expected_error

            try:
                body = self.body_model.model_validate(event.args[0])
            except ValidationError as e:
                raise EventBodyException(e)

            for field_name, parameter_names in self.body_destinations:
                # TODO replace fallback with error or warning
                value = getattr(body, field_name, None)
                yield from ((name, value) for name in parameter_names)


class AsyncEventHandler(BaseAsyncHandlerWithArguments):
    def __init__(
        self,
        async_callable: Callable[..., Awaitable[Any]],
        marker_destinations: list[tuple[Marker[Any], list[str]]],
        body_model: type[BaseModel] | None,
        body_destinations: list[tuple[str, list[str]]],
        possible_exceptions: set[EventException],
        ack_packager: CodedPackager[Any],
    ) -> None:
        super().__init__(
            async_callable=async_callable,
            marker_destinations=marker_destinations,
            body_model=body_model,
            body_destinations=body_destinations,
            possible_exceptions=possible_exceptions,
        )
        self.ack_packager = ack_packager

    async def __call__(self, event: ClientEvent) -> DataOrTuple:
        try:
            kwargs: dict[str, Any] = dict(self.parse_args(event))
        except EventException as e:
            return self.error_packager.pack_data(e)

        kwargs.update(self.build_markers(event))

        try:
            result = await self.async_callable(**kwargs)
        except EventException as e:
            if e not in self.possible_exceptions:
                warn(UndocumentedExceptionWarning(e))
            return self.error_packager.pack_data(e)

        # TODO error handling on ack packing for clarity
        return self.ack_packager.pack_data(result)


class AsyncConnectHandler(BaseAsyncHandlerWithArguments):
    async def __call__(self, event: ClientEvent) -> DataOrTuple:
        # Here `event.args` has at most one argument

        try:
            kwargs: dict[str, Any] = dict(self.parse_args(event))
        except EventException as e:
            raise ConnectionRefusedError(self.error_packager.pack_data(e))

        kwargs.update(self.build_markers(event))

        try:
            await self.async_callable(**kwargs)
        except EventException as e:
            if e not in self.possible_exceptions:
                warn(UndocumentedExceptionWarning(e))
            raise ConnectionRefusedError(self.error_packager.pack_data(e))

        return None


class AsyncDisconnectHandler(BaseAsyncHandler):
    async def __call__(self, event: ClientEvent) -> DataOrTuple:
        # Here `event.args` is always empty
        kwargs = dict(self.build_markers(event))
        await self.async_callable(**kwargs)
        return None
