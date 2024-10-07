from rest_framework import serializers
from .models import *
from notifications.models import Notification


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "description", "contact_info", "owner"]


class SimpleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "balance"]


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class TransactionSerializer(serializers.ModelSerializer):
    target = SimpleItemSerializer()

    class Meta:
        model = Transaction
        fields = ["id", "target", "price"]


class NotificationSerializer(serializers.ModelSerializer):
    actor = PublicUserSerializer()
    action_object = TransactionSerializer()

    class Meta:
        model = Notification
        fields = ["id", "unread", "actor", "action_object", "timestamp"]
