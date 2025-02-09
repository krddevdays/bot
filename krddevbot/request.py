import ssl
import typing

import httpx

from httpx import AsyncClient, Limits, AsyncBaseTransport, ASGITransport, AsyncHTTPTransport
from httpx._config import DEFAULT_LIMITS
from httpx._types import CertTypes
from telegram.request._httpxrequest import HTTPXRequest

RETRY_TIMES_DEFAULTS = 5


class HttpxAsyncClient(AsyncClient):
    def _init_transport(
        self,
        verify: ssl.SSLContext | str | bool = True,
        cert: typing.Optional[CertTypes] = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        transport: typing.Optional[AsyncBaseTransport] = None,
        app: typing.Optional[typing.Callable[..., typing.Any]] = None,
        trust_env: bool = True,
    ) -> AsyncBaseTransport:
        if transport is not None:
            return transport

        if app is not None:
            return ASGITransport(app=app)

        return AsyncHTTPTransport(
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
            retries=RETRY_TIMES_DEFAULTS,
        )


class HTTPXRequestWithRetry(HTTPXRequest):
    TIMEOUT = 60.0

    def __init__(self, *args, **kwargs):
        super().__init__(read_timeout=self.TIMEOUT, write_timeout=self.TIMEOUT, connect_timeout=self.TIMEOUT, *args, **kwargs)

    def _build_client(self) -> httpx.AsyncClient:
        return HttpxAsyncClient(**self._client_kwargs)  # type: ignore[arg-type]
