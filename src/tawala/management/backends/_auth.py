"""Custom authentication backends."""

from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpRequest

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

__all__: list[str] = ["UsernameOrEmailAuthBackend"]


class UsernameOrEmailAuthBackend(ModelBackend):
    """Allows login with either username or email."""

    def authenticate(
        self, request: HttpRequest | None, username: str | None = None, password: str | None = None, **kwargs: Any
    ) -> "AbstractBaseUser | None":
        """Authenticate user with username or email."""
        if username is None or password is None:
            return None
        User = get_user_model()
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            # Run the default password hasher to mitigate timing attacks
            User().set_password(User.objects.make_random_password())
            return None
