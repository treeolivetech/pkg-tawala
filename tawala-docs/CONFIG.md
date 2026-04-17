# Tawala Configuration Reference

A generated reference of all supported `tool.tawala` settings, their defaults, and allowed values.

Generated on: 2026-04-18 13:11:16Z

## Source Priority

Configuration is resolved in this order:

1. Environment variables
2. `pyproject.toml` in `[tool.tawala]`
3. Schema defaults

## Security & Deployment

| Key                     | TOML Path               | ENV                     | Type   | Default                                                    | Options       | Description                                                                 |
| ----------------------- | ----------------------- | ----------------------- | ------ | ---------------------------------------------------------- | ------------- | --------------------------------------------------------------------------- |
| `allowed_hosts`         | `allowed_hosts`         | `ALLOWED_HOSTS`         | `list` | `[localhost, 127.0.0.1]`                                   | -             | `List of hostnames the app is allowed to serve.`                            |
| `secret_key`            | `secret_key`            | `SECRET_KEY`            | `str`  | `django-insecure-change-me-in-production-via-env-variable` | -             | `Secret key used for cryptographic signing. Always set this in production.` |
| `debug`                 | `debug`                 | `DEBUG`                 | `bool` | `true`                                                     | `true, false` | `Enable debug mode. Keep disabled in production environments.`              |
| `secure_ssl_redirect`   | `secure_ssl_redirect`   | `SECURE_SSL_REDIRECT`   | `bool` | `false`                                                    | `true, false` | `Redirect all HTTP requests to HTTPS when enabled.`                         |
| `session_cookie_secure` | `session_cookie_secure` | `SESSION_COOKIE_SECURE` | `bool` | `false`                                                    | `true, false` | `Mark session cookies as secure so they are sent only over HTTPS.`          |
| `csrf_cookie_secure`    | `csrf_cookie_secure`    | `CSRF_COOKIE_SECURE`    | `bool` | `false`                                                    | `true, false` | `Mark CSRF cookies as secure so they are sent only over HTTPS.`             |
| `secure_hsts_seconds`   | `secure_hsts_seconds`   | `SECURE_HSTS_SECONDS`   | `int`  | `0`                                                        | -             | `HTTP Strict Transport Security max-age value in seconds.`                  |

## Presets & Storages

| Key      | TOML Path       | ENV                     | Type  | Default                                                     | Options           | Description                                                                   |
| -------- | --------------- | ----------------------- | ----- | ----------------------------------------------------------- | ----------------- | ----------------------------------------------------------------------------- |
| `option` | `preset.option` | `PRESET_OPTION`         | `str` | `default`                                                   | `default, vercel` | `Deployment preset that controls opinionated defaults for the project.`       |
| `token`  | `preset.token`  | `BLOB_READ_WRITE_TOKEN` | `str` | `get-from-vercel-blob-storage-and-keep-private-via-env-var` | -                 | `Token used for blob storage read/write access when blob support is enabled.` |

## Databases

| Key           | TOML Path        | ENV                   | Type   | Default  | Options                                                    | Description                                                                   |
| ------------- | ---------------- | --------------------- | ------ | -------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `option`      | `db.option`      | `DB_OPTION`           | `str`  | `sqlite` | `sqlite, postgresql`                                       | `Database backend to use, such as SQLite or PostgreSQL.`                      |
| `pg_use_vars` | `db.pg_use_vars` | `DB_USE_VARS_OPTION`  | `bool` | `false`  | `true, false`                                              | `Enable reading PostgreSQL connection values from individual DB_* variables.` |
| `pg_service`  | `db.pg_service`  | `DB_PGSERVICE`        | `str`  |          | -                                                          | `PostgreSQL service name from pg_service.conf, if used.`                      |
| `pg_user`     | `db.pg_user`     | `DB_PGUSER`           | `str`  |          | -                                                          | `PostgreSQL username for database authentication.`                            |
| `pg_password` | `db.pg_password` | `DB_PGPASSWORD`       | `str`  |          | -                                                          | `PostgreSQL password for database authentication.`                            |
| `pg_database` | `db.pg_database` | `DB_PGDATABASE`       | `str`  |          | -                                                          | `PostgreSQL database name to connect to.`                                     |
| `pg_host`     | `db.pg_host`     | `DB_PGHOST`           | `str`  |          | -                                                          | `PostgreSQL host or socket location.`                                         |
| `pg_port`     | `db.pg_port`     | `DB_PGPORT`           | `int`  | `5432`   | -                                                          | `PostgreSQL server port.`                                                     |
| `pg_pool`     | `db.pg_pool`     | `DB_PGPOOL_OPTION`    | `bool` | `false`  | `true, false`                                              | `Enable PostgreSQL connection pooling when supported.`                        |
| `pg_sslmode`  | `db.pg_sslmode`  | `DB_PGSSLMODE_OPTION` | `str`  | `prefer` | `disabled, allow, prefer, require, verify-ca, verify-full` | `PostgreSQL SSL mode for transport security.`                                 |

## Layout

| Key                 | TOML Path                  | ENV                               | Type   | Default | Options       | Description                                                 |
| ------------------- | -------------------------- | --------------------------------- | ------ | ------- | ------------- | ----------------------------------------------------------- |
| `option`            | `layout.option`            | `LAYOUT_OPTION`                   | `str`  | `base`  | `base, wip`   | `Primary layout template option used by the app.`           |
| `always_show_admin` | `layout.always_show_admin` | `LAYOUT_ALWAYS_SHOW_ADMIN_OPTION` | `bool` | `false` | `true, false` | `Force admin links to display regardless of debug context.` |

## Internationalization

| Key             | TOML Path                            | ENV             | Type   | Default          | Options | Description                                            |
| --------------- | ------------------------------------ | --------------- | ------ | ---------------- | ------- | ------------------------------------------------------ |
| `language_code` | `internationalization.language_code` | `LANGUAGE_CODE` | `str`  | `en-us`          | -       | `Default language code used for internationalization.` |
| `time_zone`     | `internationalization.time_zone`     | `TIME_ZONE`     | `str`  | `Africa/Nairobi` | -       | `Default time zone used for date/time handling.`       |
| `use_i18n`      | `internationalization.use_i18n`      | `USE_I18N`      | `bool` | `true`           | -       | `Enable translation and locale machinery.`             |
| `use_tz`        | `internationalization.use_tz`        | `USE_TZ`        | `bool` | `true`           | -       | `Store and handle datetimes as timezone-aware values.` |

## Runcommands

| Key       | TOML Path             | ENV                   | Type   | Default                                                                           | Options | Description                                                    |
| --------- | --------------------- | --------------------- | ------ | --------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------- |
| `install` | `runcommands.install` | `RUNCOMMANDS_INSTALL` | `list` | `[]`                                                                              | -       | `Management commands to run during project install/bootstrap.` |
| `build`   | `runcommands.build`   | `RUNCOMMANDS_BUILD`   | `list` | `[makemigrations, migrate, compilescss, collectstatic --noinput --ignore=*.scss]` | -       | `Management commands to run during build/deploy preparation.`  |
