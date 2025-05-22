from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

CHOICES_DICT = {
    "F": "Finished",
    "IP": "In progress",
    "D": "Dropped"
}

BOOK_CHOICES = {
    "TB": "Traditional book",
    "LN": "Light novel",
    "WN": "Web novel",
    "CS": "Comics",
    "MA": "Manga",
    "FF": "Fan fiction"
}

SERIES_CHOICES = {
    "SO": "Spin-off",
    "AY": "Anthology",
    "AD": "Adaptation"
}


class Creator(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        ordering = ("first_name",)


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)


class MediaUser(AbstractUser):
    class Meta:
        ordering = ("username",)


class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateField(null=True, blank=True)
    creators = models.ManyToManyField(Creator, related_name="media")
    users = models.ManyToManyField(MediaUser, through='UserMediaRating')

    class Meta:
        ordering = ("title",)


class UserMediaRating(models.Model):
    user = models.ForeignKey(MediaUser, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    review = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=CHOICES_DICT)

    class Meta:
        constraints = [
            UniqueConstraint(name="unique_reviews", fields=("user", "media"))
        ]


class Film(Media):
    country = models.CharField(max_length=255)
    duration = models.TimeField()


class Book(Media):
    chapters = models.IntegerField()
    type = models.CharField(max_length=65, choices=BOOK_CHOICES)


class Series(Media):
    country = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=CHOICES_DICT)
    seasons = models.IntegerField()
    series_number = models.IntegerField()
    type = models.CharField(max_length=65, choices=SERIES_CHOICES)
