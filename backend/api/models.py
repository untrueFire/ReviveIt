from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager
from .utils import generate_avatar


class Image(models.Model):
    filename = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.filename


def default_avatar(username: str):
    if not username:
        return Image.objects.get_or_create(filename="default_avatar.png")[0]
    if not Image.objects.filter(filename=f"{username}_avatar.png").exists():
        generate_avatar(username)
    return Image.objects.get_or_create(filename=f"{username}_avatar.png")[0]


class User(AbstractUser):
    balance = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    avatar = models.ForeignKey("Image", on_delete=models.SET_NULL, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    @property
    def group(self):
        return "admin" if self.is_staff else ("user" if self.is_active else "guest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_staff:
            self.is_active = True
        self.avatar = default_avatar(self.username)


class ItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)  # 软删除


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = TaggableManager()
    contactInfo = models.CharField(max_length=200)
    owner: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    deleted = models.BooleanField(default=False)

    objects = ItemManager()

    def delete(self):
        self.deleted = True
        self.save()


class Transaction(models.Model):
    buyer: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.ForeignKey(Item, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seller = self.target.owner
