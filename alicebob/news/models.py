from enum import Enum

from django.db import models

from model_utils.models import TimeStampedModel


class NewsState(Enum):
    BACKLOG = "BACKLOG"
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    REVIEW = "REVIEW"


class NewsTag(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    color = models.CharField(max_length=40, default="blue")
    color_code = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "tags_news"


class NewsProvider(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        db_table = "news_providers"


class NewsChannel(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    provider = models.ForeignKey(NewsProvider, on_delete=models.CASCADE, related_name="channels")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"
        db_table = "news_channels"


class EzycourseChannels(Enum):
    GENERAL = "GENERAL"
    EVENTOS = "EVENTOS"
    API_REST = "API_REST"
    IA = "IA"
    NOTICIAS = "NOTICIAS"
    TOP_CVES = "TOP_CVES"


class News(TimeStampedModel, models.Model):
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(help_text="The full content of the news")
    url = models.URLField(blank=True, null=True, help_text="URL to the news")
    image = models.URLField(blank=True, null=True, help_text="URL to the image")

    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True)
    scheduled = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(NewsTag, blank=True)
    state = models.CharField(max_length=40, choices=[(state.name, state.value) for state in NewsState], default=NewsState.BACKLOG)
    origin = models.ForeignKey(NewsChannel, on_delete=models.CASCADE, related_name="news")

    linkedin_text = models.TextField(blank=True, null=True)
    twitter_text = models.TextField(blank=True, null=True)
    telegram_text = models.TextField(blank=True, null=True)
    ezy_text = models.TextField(blank=True, null=True)

    ezycourse_channel = models.CharField(
        max_length=40, choices=[(channel.name, channel.value) for channel in EzycourseChannels],
        default=EzycourseChannels.GENERAL
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "news"
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["created"]
