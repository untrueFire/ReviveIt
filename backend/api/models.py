from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager


class User(AbstractUser):
    balance = models.PositiveIntegerField(default=0)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


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
