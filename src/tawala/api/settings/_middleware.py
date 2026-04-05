__all__ = ["MIDDLEWARE"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "django_http_compression.middleware.HttpCompressionMiddleware",  # Before any that modify html
    "django_minify_html.middleware.MinifyHtmlMiddleware",  # After http_compression, before HTML modifiers
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]
