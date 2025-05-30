import re
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy

from app.managers import UserProfileManager

ARTICLE_STATUS = (
    ("draft", "draft"),
    ("inprogress", "in progress"),
    ("published", "published"),
)


class UserProfile(AbstractUser):
    email = models.EmailField(
        gettext_lazy("email address"), max_length=255, unique=True
    )

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def article_count(self):
        return self.articles.count()

    @property
    def written_words(self):
        return self.articles.aggregate(models.Sum("word_count"))["word_count__sum"] or 0


class Article(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Article")
        verbose_name_plural = gettext_lazy("Articles")

    title = models.CharField(gettext_lazy("title"), max_length=100)
    content = models.TextField(gettext_lazy("content"), blank=True, default="")
    word_count = models.IntegerField(gettext_lazy("word count"), blank=True, default="")
    twitter_post = models.TextField(
        gettext_lazy("twitter post"), blank=True, default=""
    )
    status = models.CharField(
        gettext_lazy("status"),
        max_length=20,
        choices=ARTICLE_STATUS,
        default="draft",
    )
    created_at = models.DateTimeField(gettext_lazy("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(gettext_lazy("updated at"), auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=gettext_lazy("creator"),
        on_delete=models.CASCADE,
        related_name="articles",
    )

    def save(self, *args, **kwargs):
        text = re.sub(r"<[^>]*>", "", self.content).replace("&nbsp;", " ")
        self.word_count = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
