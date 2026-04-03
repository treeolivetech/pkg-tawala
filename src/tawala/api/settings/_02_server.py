"""Server (ASGI/WSGI) Configuration."""

from ... import DefaultApps
from .. import ConfField, SettingsConf

__all__ = ["SERVER_USE_ASGI", "WSGI_APPLICATION"]


class _ServerConf(SettingsConf):
    """Server (ASGI/WSGI) Configuration."""

    verbose_name = "02. Server (ASGI/WSGI) Configuration"

    use_asgi = ConfField(type=bool, env="SERVER_USE_ASGI", toml="server.use-asgi", default=False)


_SERVER = _ServerConf()

SERVER_USE_ASGI: bool = _SERVER.use_asgi
WSGI_APPLICATION: str = f"{DefaultApps.API}.backends.wsgi_application"
