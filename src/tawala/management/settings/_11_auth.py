"""Authentication and Password Validation Configuration.

https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
"""

from typing import TypedDict, cast

from ..conf import BaseConf, ConfField

__all__: list[str] = ["AUTH_PASSWORD_VALIDATORS"]


class _AuthPasswordValidatorsConf(BaseConf):
    """Password Validators Configuration."""

    verbose_name = "11. Password Validators Configuration"

    extend = ConfField(type=list, env="AUTH_PASSWORD_VALIDATORS_EXTEND", toml="auth.password-validators.extend", default=[])
    remove = ConfField(type=list, env="AUTH_PASSWORD_VALIDATORS_REMOVE", toml="auth.password-validators.remove", default=[])


_AUTH_PASSWORD_VALIDATORS_CONF = _AuthPasswordValidatorsConf()


class _PasswordValidatorDict(TypedDict):
    """Password validator entry."""

    NAME: str


# Work with strings for all operations
_base_validators: list[str] = [
    f"django.contrib.auth.password_validation.{validator}"
    for validator in [
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    ]
]

# Process removals (supports both the full path and just the class name)
_remove_list: set[str] = set(cast(list[str], _AUTH_PASSWORD_VALIDATORS_CONF.remove))

_filtered_validators: list[str] = [
    validator for validator in _base_validators if validator not in _remove_list and validator.split(".")[-1] not in _remove_list
]

# Append extensions
_final_validators: list[str] = _filtered_validators + cast(list[str], _AUTH_PASSWORD_VALIDATORS_CONF.extend)

# Convert the final list of strings into the dict structure Django expects
AUTH_PASSWORD_VALIDATORS: list[_PasswordValidatorDict] = [{"NAME": validator} for validator in _final_validators]
