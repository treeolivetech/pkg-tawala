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
