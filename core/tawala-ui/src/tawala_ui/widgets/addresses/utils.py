"""Widget Addresses enums."""

from enum import StrEnum

from django.db import models


class _SocialMediaPlatform(StrEnum):
    """Canonical social media platform values used across the addresses widget."""

    FACEBOOK = "facebook"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"
    SNAPCHAT = "snapchat"
    DISCORD = "discord"
    TELEGRAM = "telegram"
    GITHUB = "github"
    REDDIT = "reddit"
    TWITCH = "twitch"

    @property
    def label(self) -> str:
        """Return a human-readable label for the platform."""
        return _SOCIAL_MEDIA_LABELS[self]

    @property
    def icon_class(self) -> str:
        """Return the Bootstrap icon class for the platform."""
        return _SOCIAL_MEDIA_ICON_CLASSES[self]

    @property
    def base_url(self) -> str:
        """Return the base profile URL for the platform (without username)."""
        return _SOCIAL_MEDIA_BASE_URLS[self]

    @property
    def uses_at_prefix(self) -> bool:
        """Return True if the platform username must be prefixed with '@'."""
        return self in _SOCIAL_MEDIA_AT_PREFIX

    def build_profile_url(self, username: str) -> str:
        """Return the full profile URL for the given username.

        Strips a leading '@' from the username before concatenation because
        the base URL already encodes the '@' where required (e.g. YouTube,
        TikTok).  This keeps the stored username consistent regardless of
        whether the user typed it with or without the symbol.
        """
        clean = (
            username.lstrip("@") if not self.uses_at_prefix else username.lstrip("@")
        )
        return f"{self.base_url}{'@' if self.uses_at_prefix else ''}{clean}"


_SOCIAL_MEDIA_LABELS: dict[_SocialMediaPlatform, str] = {
    _SocialMediaPlatform.FACEBOOK: "Facebook",
    _SocialMediaPlatform.TWITTER: "X (formerly Twitter)",
    _SocialMediaPlatform.INSTAGRAM: "Instagram",
    _SocialMediaPlatform.LINKEDIN: "LinkedIn",
    _SocialMediaPlatform.YOUTUBE: "YouTube",
    _SocialMediaPlatform.TIKTOK: "TikTok",
    _SocialMediaPlatform.PINTEREST: "Pinterest",
    _SocialMediaPlatform.SNAPCHAT: "Snapchat",
    _SocialMediaPlatform.DISCORD: "Discord",
    _SocialMediaPlatform.TELEGRAM: "Telegram",
    _SocialMediaPlatform.GITHUB: "GitHub",
    _SocialMediaPlatform.REDDIT: "Reddit",
    _SocialMediaPlatform.TWITCH: "Twitch",
}

_SOCIAL_MEDIA_ICON_CLASSES: dict[_SocialMediaPlatform, str] = {
    _SocialMediaPlatform.FACEBOOK: "bi bi-facebook",
    _SocialMediaPlatform.TWITTER: "bi bi-twitter-x",
    _SocialMediaPlatform.INSTAGRAM: "bi bi-instagram",
    _SocialMediaPlatform.LINKEDIN: "bi bi-linkedin",
    _SocialMediaPlatform.YOUTUBE: "bi bi-youtube",
    _SocialMediaPlatform.TIKTOK: "bi bi-tiktok",
    _SocialMediaPlatform.PINTEREST: "bi bi-pinterest",
    _SocialMediaPlatform.SNAPCHAT: "bi bi-snapchat",
    _SocialMediaPlatform.DISCORD: "bi bi-discord",
    _SocialMediaPlatform.TELEGRAM: "bi bi-telegram",
    _SocialMediaPlatform.GITHUB: "bi bi-github",
    _SocialMediaPlatform.REDDIT: "bi bi-reddit",
    _SocialMediaPlatform.TWITCH: "bi bi-twitch",
}

# Base profile URLs for each platform. Do NOT include a trailing '@'; that is
# handled by `_SOCIAL_MEDIA_AT_PREFIX` so the username storage stays clean.
_SOCIAL_MEDIA_BASE_URLS: dict[_SocialMediaPlatform, str] = {
    _SocialMediaPlatform.FACEBOOK: "https://www.facebook.com/",
    _SocialMediaPlatform.TWITTER: "https://x.com/",
    _SocialMediaPlatform.INSTAGRAM: "https://www.instagram.com/",
    _SocialMediaPlatform.LINKEDIN: "https://www.linkedin.com/in/",
    _SocialMediaPlatform.YOUTUBE: "https://www.youtube.com/",
    _SocialMediaPlatform.TIKTOK: "https://www.tiktok.com/",
    _SocialMediaPlatform.PINTEREST: "https://www.pinterest.com/",
    _SocialMediaPlatform.SNAPCHAT: "https://www.snapchat.com/add/",
    _SocialMediaPlatform.DISCORD: "https://discord.gg/",
    _SocialMediaPlatform.TELEGRAM: "https://t.me/",
    _SocialMediaPlatform.GITHUB: "https://github.com/",
    _SocialMediaPlatform.REDDIT: "https://www.reddit.com/user/",
    _SocialMediaPlatform.TWITCH: "https://www.twitch.tv/",
}

# Platforms whose usernames are conventionally written with a leading '@'
# (e.g. @channelname on YouTube, @handle on TikTok).  The save() method on
# Social will auto-prepend '@' for these if the user omits it.
_SOCIAL_MEDIA_AT_PREFIX: frozenset[_SocialMediaPlatform] = frozenset({
    _SocialMediaPlatform.YOUTUBE,
    _SocialMediaPlatform.TIKTOK,
})


class SocialMediaPlatformChoice(models.TextChoices):
    """Django-compatible social media choices for model fields."""

    FACEBOOK = _SocialMediaPlatform.FACEBOOK.value, _SocialMediaPlatform.FACEBOOK.label
    TWITTER = _SocialMediaPlatform.TWITTER.value, _SocialMediaPlatform.TWITTER.label
    INSTAGRAM = (
        _SocialMediaPlatform.INSTAGRAM.value,
        _SocialMediaPlatform.INSTAGRAM.label,
    )
    LINKEDIN = _SocialMediaPlatform.LINKEDIN.value, _SocialMediaPlatform.LINKEDIN.label
    YOUTUBE = _SocialMediaPlatform.YOUTUBE.value, _SocialMediaPlatform.YOUTUBE.label
    TIKTOK = _SocialMediaPlatform.TIKTOK.value, _SocialMediaPlatform.TIKTOK.label
    PINTEREST = (
        _SocialMediaPlatform.PINTEREST.value,
        _SocialMediaPlatform.PINTEREST.label,
    )
    SNAPCHAT = _SocialMediaPlatform.SNAPCHAT.value, _SocialMediaPlatform.SNAPCHAT.label
    DISCORD = _SocialMediaPlatform.DISCORD.value, _SocialMediaPlatform.DISCORD.label
    TELEGRAM = _SocialMediaPlatform.TELEGRAM.value, _SocialMediaPlatform.TELEGRAM.label
    GITHUB = _SocialMediaPlatform.GITHUB.value, _SocialMediaPlatform.GITHUB.label
    REDDIT = _SocialMediaPlatform.REDDIT.value, _SocialMediaPlatform.REDDIT.label
    TWITCH = _SocialMediaPlatform.TWITCH.value, _SocialMediaPlatform.TWITCH.label

    @classmethod
    def icon_for_value(cls, value: str) -> str:
        """Return the icon class for a given choice value."""
        try:
            return _SocialMediaPlatform(value).icon_class
        except ValueError:
            return ""

    @classmethod
    def base_url_for_value(cls, value: str) -> str:
        """Return the base profile URL for a given choice value."""
        try:
            return _SocialMediaPlatform(value).base_url
        except ValueError:
            return ""

    @classmethod
    def build_profile_url_for_value(cls, value: str, username: str) -> str:
        """Return the full profile URL for a given platform value and username."""
        try:
            return _SocialMediaPlatform(value).build_profile_url(username)
        except ValueError:
            return ""

    @classmethod
    def uses_at_prefix_for_value(cls, value: str) -> bool:
        """Return True if the platform requires a leading '@' in its username."""
        try:
            return _SocialMediaPlatform(value).uses_at_prefix
        except ValueError:
            return False
