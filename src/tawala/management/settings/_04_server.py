"""Server (ASGI/WSGI) Configuration."""

from ...constants import Package
from ..conf import BaseConf, ConfField

__all__: list[str] = ["SERVER_USE_ASGI", "ASGI_APPLICATION", "WSGI_APPLICATION"]


class _ServerConf(BaseConf):
    """Server (ASGI/WSGI) Configuration."""

    verbose_name = "04. Server (ASGI/WSGI) Configuration"

    use_asgi = ConfField(type=bool, env="SERVER_USE_ASGI", toml="server.use-asgi", default=False)


_SERVER = _ServerConf()

SERVER_USE_ASGI: bool = _SERVER.use_asgi
ASGI_APPLICATION: str = f"{Package.NAME}.management.backends.asgi_application"
WSGI_APPLICATION: str = f"{Package.NAME}.management.backends.wsgi_application"
