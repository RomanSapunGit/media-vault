from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint


class StatusChoices(models.TextChoices):
    FINISHED = "F", "Finished"
    IN_PROGRESS = "IP", "In progress"
    DROPPED = "D", "Dropped"


class Creator(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("first_name",)


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class MediaUser(AbstractUser):
    class Meta:
        ordering = ("username",)


class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(
        validators=[
            MinLengthValidator(
                50,
                "Description must be at least 50 symbols"
            ),
            MaxLengthValidator(
                4000,
                "Description must be less than 4000 symbols"
            )
        ]
    )
    created_at = models.DateField(null=True, blank=True)
    creators = models.ManyToManyField(
        Creator,
        related_name="media",
        blank=True
    )
    users = models.ManyToManyField(
        MediaUser,
        through='UserMediaRating',
        related_name="rated_media")
    genres = models.ManyToManyField(Genre, related_name="media")

    class Meta:
        ordering = ("title",)


class UserMediaRating(models.Model):
    user = models.ForeignKey(MediaUser, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        null=True,
        blank=True
    )
    review = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoices.choices)
    is_hidden = models.BooleanField()

    class Meta:
        constraints = [
            UniqueConstraint(name="unique_reviews", fields=("user", "media"))
        ]
        db_table = "user_media_rating"


class Film(Media):
    country = models.CharField(max_length=255)
    duration = models.TimeField()


class Book(Media):
    class BookTypeChoices(models.TextChoices):
        TRADITIONAL = "TB", "Traditional book"
        LIGHT_NOVEL = "LN", "Light novel"
        WEB_NOVEL = "WN", "Web novel"
        COMICS = "CS", "Comics"
        MANGA = "MA", "Manga"
        FAN_FICTION = "FF", "Fan fiction"

    chapters = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=65, choices=BookTypeChoices.choices)


class Series(Media):
    class SeriesChoices(models.TextChoices):
        SPIN_OFF = "SO", "Spin-off",
        ANTHOLOGY = "AY", "Anthology",
        ADAPTATION = "AD", "Adaptation"
        ANIME = "AE", "Anime"

    country = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=StatusChoices.choices)
    seasons = models.PositiveSmallIntegerField()
    series_number = models.PositiveIntegerField()
    type = models.CharField(max_length=65, choices=SeriesChoices.choices)
