from notifications.models import Notification
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["filename"]

class UserSerializer(serializers.ModelSerializer):
    avatar = ImageSerializer()
    class Meta:
        model = User
        fields = ["id", "username", "balance", "group", "avatar"]
        extra_kwargs = {
            'group': {'help_text': '用户组，guest 为临时用户，user 为正式用户，admin 为管理员'},
        }
    

class PublicUserSerializer(serializers.ModelSerializer):
    """
    公开视图，不展示敏感信息（余额）
    """
    avatar = ImageSerializer()
    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = PublicUserSerializer(read_only=True)  # 通过设置只读，允许了嵌套序列化器的反序列化（在 `update_item` 中使用）
    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ["id", "name", "description", "contactInfo", "owner", "tags"]


class SimpleItemSerializer(serializers.ModelSerializer):
    """
    简化的物品视图，仅供外键序列化使用
    """

    class Meta:
        model = Item
        fields = ["id", "name"]


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
        fields = ["id", "unread", "actor", "verb", "action_object", "timestamp", "data"]  # data 字段存储通知的处理结果
