"""Settings schema."""

from dataclasses import dataclass, field
from typing import Any, TypeAlias, cast

from .enums import (
    DatabaseDefaults,
    DatabaseHelpTexts,
    DatabaseKeys,
    DatabaseOptions,
    DatabasePoolOptions,
    DatabaseSSlModeOptions,
    DatabaseUseVarsOptions,
    InternationalizationDefaults,
    InternationalizationHelpTexts,
    InternationalizationKeys,
    LayoutAlwaysShowAdminOptions,
    LayoutDefaults,
    LayoutHelpTexts,
    LayoutKeys,
    LayoutOptions,
    PresetDefaults,
    PresetHelpTexts,
    PresetKeys,
    PresetOptions,
    RuncommandDefaults,
    RuncommandHelpTexts,
    RuncommandKeys,
    SecurityCSRFCookieSecureOptions,
    SecurityDebugOptions,
    SecurityDefaults,
    SecurityHelpTexts,
    SecurityKeys,
    SecuritySecureSSLRedirectOptions,
    SecuritySessionCookieSecureOptions,
)


@dataclass(frozen=True)
class SchemaField:
    """Definition for a single configurable field in the settings schema."""

    type: type[Any]
    env: str
    toml: str
    default: Any
    options: list[Any] = field(default_factory=lambda: cast(list[Any], []))
    help_text: str = ""


_Schema: TypeAlias = dict[str, SchemaField]

# ============================================================================
# Module Exports
# ============================================================================
__all__ = [
    "SECURITY_SCHEMA",
    "PRESET_SCHEMA",
    "DATABASES_SCHEMA",
    "LAYOUT_SCHEMA",
    "INTERNATIONALIZATION_SCHEMA",
    "RUNCOMMANDS_SCHEMA",
]

# ============================================================================
# Security & Deployment
# ============================================================================
SECURITY_SCHEMA: _Schema = {
    SecurityKeys.ALLOWED_HOSTS: SchemaField(
        type=list,
        env="ALLOWED_HOSTS",
        toml=SecurityKeys.ALLOWED_HOSTS.value,
        default=SecurityDefaults.ALLOWED_HOSTS.value,
        help_text=SecurityHelpTexts.ALLOWED_HOSTS.value,
    ),
    SecurityKeys.SECRET_KEY: SchemaField(
        type=str,
        env="SECRET_KEY",
        toml=SecurityKeys.SECRET_KEY,
        default=SecurityDefaults.SECRET_KEY.value,
        help_text=SecurityHelpTexts.SECRET_KEY.value,
    ),
    SecurityKeys.DEBUG_OPTION: SchemaField(
        type=bool,
        env="DEBUG",
        toml=SecurityKeys.DEBUG_OPTION.value,
        default=SecurityDefaults.DEBUG_OPTION.value,
        options=list(SecurityDebugOptions),
        help_text=SecurityHelpTexts.DEBUG_OPTION,
    ),
    SecurityKeys.SECURE_SSL_REDIRECT_OPTION: SchemaField(
        type=bool,
        env="SECURE_SSL_REDIRECT",
        toml=SecurityKeys.SECURE_SSL_REDIRECT_OPTION.value,
        default=SecurityDefaults.SECURE_SSL_REDIRECT_OPTION.value,
        options=list(SecuritySecureSSLRedirectOptions),
        help_text=SecurityHelpTexts.SECURE_SSL_REDIRECT_OPTION.value,
    ),
    SecurityKeys.SESSION_COOKIE_SECURE_OPTION: SchemaField(
        type=bool,
        env="SESSION_COOKIE_SECURE",
        toml=SecurityKeys.SESSION_COOKIE_SECURE_OPTION.value,
        default=SecurityDefaults.SESSION_COOKIE_SECURE_OPTION.value,
        options=list(SecuritySessionCookieSecureOptions),
        help_text=SecurityHelpTexts.SESSION_COOKIE_SECURE_OPTION.value,
    ),
    SecurityKeys.CSRF_COOKIE_SECURE_OPTION: SchemaField(
        type=bool,
        env="CSRF_COOKIE_SECURE",
        toml=SecurityKeys.CSRF_COOKIE_SECURE_OPTION.value,
        default=SecurityDefaults.CSRF_COOKIE_SECURE_OPTION.value,
        options=list(SecurityCSRFCookieSecureOptions),
        help_text=SecurityHelpTexts.CSRF_COOKIE_SECURE_OPTION.value,
    ),
    SecurityKeys.SECURE_HSTS_SECONDS: SchemaField(
        type=int,
        env="SECURE_HSTS_SECONDS",
        toml=SecurityKeys.SECURE_HSTS_SECONDS.value,
        default=SecurityDefaults.SECURE_HSTS_SECONDS.value,
        help_text=SecurityHelpTexts.SECURE_HSTS_SECONDS.value,
    ),
}


# ============================================================================
# Preset & Storages
# ============================================================================
PRESET_SCHEMA: _Schema = {
    PresetKeys.OPTION: SchemaField(
        type=str,
        env="PRESET_OPTION",
        toml=f"{PresetKeys.PRESET.value}.{PresetKeys.OPTION.value}",
        default=PresetOptions.DEFAULT.value,
        options=list(PresetOptions),
        help_text=PresetHelpTexts.OPTION.value,
    ),
    PresetKeys.BLOB_TOKEN: SchemaField(
        type=str,
        env="BLOB_READ_WRITE_TOKEN",
        toml=f"{PresetKeys.PRESET.value}.{PresetKeys.BLOB_TOKEN.value}",
        default=PresetDefaults.BLOB_TOKEN.value,
        help_text=PresetHelpTexts.BLOB_TOKEN.value,
    ),
}


# ============================================================================
# Databases
# ============================================================================
DATABASES_SCHEMA: _Schema = {
    DatabaseKeys.OPTION: SchemaField(
        type=str,
        env="DB_OPTION",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.OPTION.value}",
        default=DatabaseDefaults.OPTION.value,
        options=list(DatabaseOptions),
        help_text=DatabaseHelpTexts.OPTION.value,
    ),
    DatabaseKeys.USE_VARS_OPTION: SchemaField(
        type=bool,
        env="DB_USE_VARS_OPTION",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.USE_VARS_OPTION.value}",
        default=DatabaseDefaults.USE_VARS_OPTION.value,
        options=list(DatabaseUseVarsOptions),
        help_text=DatabaseHelpTexts.USE_VARS_OPTION.value,
    ),
    DatabaseKeys.SERVICE: SchemaField(
        type=str,
        env="DB_PGSERVICE",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.SERVICE.value}",
        default=DatabaseDefaults.SERVICE.value,
        help_text=DatabaseHelpTexts.SERVICE.value,
    ),
    DatabaseKeys.USER: SchemaField(
        type=str,
        env="DB_PGUSER",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.USER.value}",
        default=DatabaseDefaults.USER.value,
        help_text=DatabaseHelpTexts.USER.value,
    ),
    DatabaseKeys.PASSWORD: SchemaField(
        type=str,
        env="DB_PGPASSWORD",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.PASSWORD.value}",
        default=DatabaseDefaults.PASSWORD.value,
        help_text=DatabaseHelpTexts.PASSWORD.value,
    ),
    DatabaseKeys.NAME: SchemaField(
        type=str,
        env="DB_PGDATABASE",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.NAME.value}",
        default=DatabaseDefaults.NAME.value,
        help_text=DatabaseHelpTexts.NAME.value,
    ),
    DatabaseKeys.HOST: SchemaField(
        type=str,
        env="DB_PGHOST",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.HOST.value}",
        default=DatabaseDefaults.HOST.value,
        help_text=DatabaseHelpTexts.HOST.value,
    ),
    DatabaseKeys.PORT: SchemaField(
        type=int,
        env="DB_PGPORT",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.PORT.value}",
        default=DatabaseDefaults.PORT.value,
        help_text=DatabaseHelpTexts.PORT.value,
    ),
    DatabaseKeys.POOL_OPTION: SchemaField(
        type=bool,
        env="DB_PGPOOL_OPTION",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.POOL_OPTION.value}",
        default=DatabaseDefaults.POOL_OPTION.value,
        options=list(DatabasePoolOptions),
        help_text=DatabaseHelpTexts.POOL_OPTION.value,
    ),
    DatabaseKeys.SSLMODE_OPTION: SchemaField(
        type=str,
        env="DB_PGSSLMODE_OPTION",
        toml=f"{DatabaseKeys.DB.value}.{DatabaseKeys.SSLMODE_OPTION.value}",
        default=DatabaseDefaults.SSLMODE_OPTION.value,
        options=list(DatabaseSSlModeOptions),
        help_text=DatabaseHelpTexts.SSLMODE_OPTION.value,
    ),
}


# ============================================================================
# Layout
# ============================================================================
LAYOUT_SCHEMA: _Schema = {
    LayoutKeys.OPTION: SchemaField(
        type=str,
        env="LAYOUT_OPTION",
        toml=f"{LayoutKeys.LAYOUT.value}.{LayoutKeys.OPTION.value}",
        default=LayoutDefaults.OPTION.value,
        options=list(LayoutOptions),
        help_text=LayoutHelpTexts.OPTION.value,
    ),
    LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION: SchemaField(
        type=bool,
        env="LAYOUT_ALWAYS_SHOW_ADMIN_OPTION",
        toml=f"{LayoutKeys.LAYOUT.value}.{LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION.value}",
        default=LayoutDefaults.ALWAYS_SHOW_ADMIN_OPTION.value,
        options=list(LayoutAlwaysShowAdminOptions),
        help_text=LayoutHelpTexts.ALWAYS_SHOW_ADMIN_OPTION.value,
    ),
}


# ============================================================================
# Internationalization
# ============================================================================
INTERNATIONALIZATION_SCHEMA: _Schema = {
    InternationalizationKeys.LANGUAGE_CODE: SchemaField(
        type=str,
        env="LANGUAGE_CODE",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION.value}.{InternationalizationKeys.LANGUAGE_CODE.value}",
        default=InternationalizationDefaults.LANGUAGE_CODE.value,
        help_text=InternationalizationHelpTexts.LANGUAGE_CODE.value,
    ),
    InternationalizationKeys.TIME_ZONE: SchemaField(
        type=str,
        env="TIME_ZONE",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION.value}.{InternationalizationKeys.TIME_ZONE.value}",
        default=InternationalizationDefaults.TIME_ZONE.value,
        help_text=InternationalizationHelpTexts.TIME_ZONE.value,
    ),
    InternationalizationKeys.USE_I18N: SchemaField(
        type=bool,
        env="USE_I18N",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION.value}.{InternationalizationKeys.USE_I18N.value}",
        default=InternationalizationDefaults.USE_I18N.value,
        help_text=InternationalizationHelpTexts.USE_I18N.value,
    ),
    InternationalizationKeys.USE_TZ: SchemaField(
        type=bool,
        env="USE_TZ",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION.value}.{InternationalizationKeys.USE_TZ.value}",
        default=InternationalizationDefaults.USE_TZ.value,
        help_text=InternationalizationHelpTexts.USE_TZ.value,
    ),
}


# ============================================================================
# Runcommands
# ============================================================================
RUNCOMMANDS_SCHEMA: _Schema = {
    RuncommandKeys.INSTALL: SchemaField(
        type=list,
        env="RUNCOMMANDS_INSTALL",
        toml=f"{RuncommandKeys.RUNCOMMANDS.value}.{RuncommandKeys.INSTALL.value}",
        default=RuncommandDefaults.INSTALL.value,
        help_text=RuncommandHelpTexts.INSTALL.value,
    ),
    RuncommandKeys.BUILD: SchemaField(
        type=list,
        env="RUNCOMMANDS_BUILD",
        toml=f"{RuncommandKeys.RUNCOMMANDS.value}.{RuncommandKeys.BUILD.value}",
        default=RuncommandDefaults.BUILD.value,
        help_text=RuncommandHelpTexts.BUILD.value,
    ),
}
