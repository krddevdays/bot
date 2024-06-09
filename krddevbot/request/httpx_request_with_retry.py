import httpx

from typing import Collection, Optional, Union

from telegram._utils.types import HTTPVersion, SocketOpt
from telegram.request._httpxrequest import HTTPXRequest

RETRY_TIMES_DEFAULTS = 5


class HTTPXRequestWithRetry(HTTPXRequest):
    def __init__(
        self,
        connection_pool_size: int = 1,
        read_timeout: Optional[float] = 5.0,
        write_timeout: Optional[float] = 5.0,
        connect_timeout: Optional[float] = 5.0,
        pool_timeout: Optional[float] = 1.0,
        http_version: HTTPVersion = "1.1",
        socket_options: Optional[Collection[SocketOpt]] = None,
        proxy: Optional[Union[str, httpx.Proxy, httpx.URL]] = None,
        retries: int = RETRY_TIMES_DEFAULTS,
    ):
        self._http_version = http_version
        timeout = httpx.Timeout(
            connect=connect_timeout,
            read=read_timeout,
            write=write_timeout,
            pool=pool_timeout,
        )
        limits = httpx.Limits(
            max_connections=connection_pool_size,
            max_keepalive_connections=connection_pool_size,
        )

        if http_version not in ("1.1", "2", "2.0"):
            raise ValueError("`http_version` must be either '1.1', '2.0' or '2'.")

        http1 = http_version == "1.1"
        http_kwargs = {"http1": http1, "http2": not http1}
        transport = (
            httpx.AsyncHTTPTransport(
                socket_options=socket_options,
                retries=retries,
            )
            if socket_options or retries
            else None
        )
        self._client_kwargs = {
            "timeout": timeout,
            "proxies": proxy,
            "limits": limits,
            "transport": transport,
            **http_kwargs,
        }

        self._client = self._build_client()
