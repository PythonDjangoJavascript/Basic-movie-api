from django.db import models


class StreamPlatform(models.Model):
    """Define Movie Streaming platform model"""
    name = models.CharField(max_length=80)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=200)

    def __str__(self) -> str:
        return self.name


class WatchList(models.Model):
    """Define Movie database"""

    title = models.CharField(max_length=100)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
