from django.db import IntegrityError
import rest_framework.request
from django.core.exceptions import RequestDataTooBig
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from notifications.signals import notify
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .messages import *
from .models import *
from .serializers import *


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("item_id", openapi.IN_PATH, description="要查询的物品ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    operation_summary="查询指定ID的物品",
    responses={200: ItemSerializer(), 404: NOT_FOUND},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_item(_, item_id):
    try:
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="返回数量上限", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter("offset", openapi.IN_QUERY, description="起始下标", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter("orderby", openapi.IN_QUERY, description="排序字段", type=openapi.TYPE_STRING, required=False),
    ],
    operation_summary="查询当前用户的物品",
    responses={200: ItemSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_items(request: rest_framework.request.Request):
    limit = int(request._request.GET.get("limit", default=100))
    offset = int(request._request.GET.get("offset", default=0))
    orderby = request._request.GET.get("orderby")
    items = request.user.item_set.all()
    if orderby:
        items = items.order_by(orderby)
    items = items[offset : offset + limit]
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


item_schema = openapi.Schema(
    title="item",
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="物品名称"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="物品描述"),
        "contactInfo": openapi.Schema(type=openapi.TYPE_STRING, description="联系人信息"),
        "tags": openapi.Schema(title="tags", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="标签"),
    },
    required=["name", "description", "contactInfo"],
)


@swagger_auto_schema(
    method="post",
    request_body=item_schema,
    operation_summary="添加物品",
    responses={200: SUCCESS, 400: INVALID_REQUEST},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_item(request: rest_framework.request.Request):
    serializer = ItemSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return fast200
    return fast400


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter("item_id", openapi.IN_PATH, description="要删除的物品ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    operation_summary="删除指定ID的物品",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: PERMISSION_DENIED, 404: NOT_FOUND},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_item(request: rest_framework.request.Request, item_id: int):
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user:
            item.delete()
            return fast200
        else:
            return fast403
    except Item.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter("item_id", openapi.IN_PATH, description="要更新的物品ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    request_body=item_schema,
    operation_summary="更新指定ID的物品",
    responses={200: ItemSerializer()},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_item(request: rest_framework.request.Request, item_id: int):
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user:
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return fast400
        else:
            return fast403
    except Item.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("q", openapi.IN_QUERY, description="物品名称或描述", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter("limit", openapi.IN_QUERY, description="返回数量上限", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter("offset", openapi.IN_QUERY, description="起始下标", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter("orderby", openapi.IN_QUERY, description="排序字段", type=openapi.TYPE_STRING, required=False),
    ],
    operation_summary="根据关键字查询物品",
    responses={200: ItemSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def search_items(request: rest_framework.request.Request):
    query = request._request.GET.get("q")
    limit = int(request._request.GET.get("limit", default=100))
    offset = int(request._request.GET.get("offset", default=0))
    orderby = request._request.GET.get("orderby")
    items = Item.objects.all()
    if orderby:
        items = items.order_by(orderby)
    if query:
        items = Item.objects.filter(name__icontains=query) | Item.objects.filter(description__icontains=query)
    serializer = ItemSerializer(items[offset : offset + limit], many=True)
    return Response(serializer.data)


@swagger_auto_schema(method="get", operation_summary="查询当前用户的信息", responses={200: UserSerializer(), 403: NO_CRED})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter("notification_id", openapi.IN_PATH, description="要同意的通知ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    operation_summary="同意指定ID的通知",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: PERMISSION_DENIED, 404: NOT_FOUND},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_deal(request: rest_framework.request.Request, notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        if not notification.unread or notification.verb != "proposed":
            return fast404
        deal: Transaction = notification.action_object
        item = deal.target
        new_owner = deal.buyer
        if new_owner != request.user and request.user == notification.recipient:
            if item.owner == request.user:
                item.owner.balance += deal.price
                item.owner.save()
                item.owner = new_owner
                item.save()
                notify.send(request.user, verb="accepted", recipient=new_owner, action_object=deal)
                notification.mark_as_read()
                notification.data = "accepted"
                notification.save()
                return fast200
            else:
                # 若已售空，退款
                buyer = deal.buyer
                buyer.balance += deal.price
                buyer.save()
                notify.send(request.user, verb="sold out", recipient=new_owner, action_object=deal)
                notification.mark_as_read()
                notification.data = "sold out"
                notification.save()
                return fast404
        else:
            return fast403
    except Notification.DoesNotExist:
        return fast400


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter("notification_id", openapi.IN_PATH, description="要拒绝的通知ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    operation_summary="拒绝指定ID的通知",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: PERMISSION_DENIED, 404: NOT_FOUND},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_deal(request: rest_framework.request.Request, notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        if not notification.unread or notification.verb != "proposed":
            return fast400
        if notification.recipient != request.user:
            return fast403
        deal: Transaction = notification.action_object
        buyer = deal.buyer
        buyer.balance += deal.price
        buyer.save()
        notify.send(request.user, verb="rejected", recipient=buyer, action_object=deal)
        notification.mark_as_read()
        notification.data = "rejected"
        notification.save()
        return fast200
    except Notification.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "price": openapi.Schema(type=openapi.TYPE_INTEGER, description="为了复活物品愿意消耗的功德"),
        },
        required=["price"],
    ),
    manual_parameters=[
        openapi.Parameter("item_id", openapi.IN_PATH, description="要复活的物品ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    operation_summary="复活指定ID的物品",
    responses={200: SUCCESS, 404: NOT_FOUND, 403: NO_BALANCE, 400: INVALID_REQUEST},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revive(request: rest_framework.request.Request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        price = int(request.data.get("price"))
        buyer: User = request.user
        if not isinstance(price, int) or price < 0:
            return fast400
        if item.owner != buyer:
            if buyer.balance >= price:
                deal = Transaction.objects.create(buyer=buyer, target=item, price=price)
                buyer.balance -= price
                buyer.save()
                notify.send(request.user, verb="proposed", action_object=deal, recipient=item.owner)
                return fast200
            else:
                return fast403
        else:
            return fast400
    except Item.DoesNotExist:
        return fast404


@swagger_auto_schema(method="get", operation_summary="获取当前用户所有通知", responses={200: NotificationSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_notifications(request: rest_framework.request.Request):
    notifications = request.user.notifications.all()
    return Response(NotificationSerializer(notifications, many=True).data)


@swagger_auto_schema(method="get", operation_summary="获取当前用户所有未读通知", responses={200: NotificationSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_notifications_unread(request: rest_framework.request.Request):
    notifications = request.user.notifications.unread()
    return Response(NotificationSerializer(notifications, many=True).data)


@swagger_auto_schema(method="get", operation_summary="获取当前用户所有已读通知", responses={200: NotificationSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_notifications_read(request: rest_framework.request.Request):
    notifications = request.user.notifications.read()
    return Response(NotificationSerializer(notifications, many=True).data)


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter("notification_id", openapi.IN_PATH, description="要标为已读的通知ID", type=openapi.TYPE_INTEGER, required=True),
    ],
    operation_summary="将指定ID的通知标为已读",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: PERMISSION_DENIED},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def read(request: rest_framework.request.Request, notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        if notification.recipient != request.user:
            return fast403
        notification.mark_as_read()
        return fast200
    except Notification.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="post",
    operation_summary="生成一个PoW（工作量证明）",
    responses={
        200: openapi.Schema(
            title="PoW",
            type=openapi.TYPE_OBJECT,
            properties={"challenge": openapi.Schema(type=openapi.TYPE_STRING), "difficulty": openapi.Schema(type=openapi.TYPE_INTEGER)},
        ),
        400: INVALID_REQUEST,
        403: NO_CRED,
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def challenge(request: rest_framework.request.Request):

    def genPoW():
        from random import choices
        from string import ascii_letters

        return "".join(choices(ascii_letters, k=16))

    chall = genPoW()
    difficulty = 4
    request._request.session["challenge"] = chall
    request._request.session["difficulty"] = difficulty
    return JsonResponse({"challenge": chall, "difficulty": difficulty})


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "nonce": openapi.Schema(type=openapi.TYPE_STRING, description="满足challenge的答案"),
        },
        required=["nonce"],
    ),
    operation_description="验证规则是`sha256(challenge + nonce)`以`difficulty`个`0`结尾",
    operation_summary="验证一个PoW",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: NO_CRED},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def knock(request: rest_framework.request.Request):

    def verify(challenge: str, nonce: str, difficulty=4):
        from hashlib import sha256

        return sha256((challenge + nonce).encode()).hexdigest().endswith("0" * difficulty)

    if "challenge" not in request._request.session:
        return fast400

    challenge: str = request._request.session["challenge"]
    difficulty: int = request._request.session["difficulty"]
    nonce: str = request.data["nonce"]
    if not isinstance(nonce, str) or not verify(challenge, nonce, difficulty):
        return fast400
    user: User = request.user
    user.balance += 1
    user.save()
    return fast200


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "item_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="物品ID"),
            "tags": openapi.Schema(title="tags", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="要添加的标签"),
        },
        required=["item_id", "tags"],
    ),
    operation_summary="为指定ID的物品添加标签",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: PERMISSION_DENIED, 404: NOT_FOUND},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_tag(request: rest_framework.request.Request):
    try:
        item_id, tags = request.data.values()
        item = Item.objects.get(id=int(item_id))
        if item.owner == request.user:
            if isinstance(tags, str):
                tags = [tags]
            item.tags.add(*list(tags))
            item.save()
            return fast200
        else:
            return fast403
    except Item.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "item_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="物品ID"),
            "tags": openapi.Schema(title="tags", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="要移除的标签"),
        },
        required=["item_id", "tags"],
    ),
    operation_summary="为指定ID的物品移除标签",
    responses={200: SUCCESS, 400: INVALID_REQUEST, 403: PERMISSION_DENIED, 404: NOT_FOUND},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_tag(request: rest_framework.request.Request):
    try:
        item_id, tags = request.data.values()
        item = Item.objects.get(id=int(item_id))
        if item.owner == request.user:
            if isinstance(tags, str):
                tags = [tags]
            item.tags.remove(*list(tags))
            item.save()
            return fast200
        else:
            return fast403
    except Item.DoesNotExist:
        return fast404


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "tags": openapi.Schema(title="tags", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="要查询的标签"),
        },
        required=["tags"],
    ),
    operation_summary="根据标签查询物品",
    responses={200: ItemSerializer(many=True), 400: INVALID_REQUEST},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def search_tag(request: rest_framework.request.Request):
    tags: str | list[str] = request.data["tags"]
    if isinstance(tags, str):
        tags = [tags]
    limit = int(request._request.GET.get("limit", default=100))
    offset = int(request._request.GET.get("offset", default=0))
    orderby = request._request.GET.get("orderby")
    items = Item.objects.filter(tags__name__in=tags).distinct()
    if orderby:
        items = items.order_by(orderby)
    serializer = ItemSerializer(items[offset : offset + limit], many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="上传一个文件，返回其URL",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['file'],
        properties={
            'file': openapi.Schema(type=openapi.TYPE_FILE, description="要上传的文件"),
        },
    ),
    responses={
        200: openapi.Response(
            description="文件上传成功",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'url': openapi.Schema(type=openapi.TYPE_STRING, description="文件的URL"),
                },
            ),
        ),
        400: INVALID_REQUEST,
        413: REQUEST_TOO_BIG,
        422: INVALID_FORMAT
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request: rest_framework.request.Request):
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': NO_FILE}, status=400)
        
        from hashlib import sha256
        from os.path import splitext
        
        file_obj = request.FILES['file']
        file_content = file_obj.read()
        
        if len(file_content) > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
            raise RequestDataTooBig
        
        _, ext = splitext(file_obj.name)
        assert ext in settings.ALLOWED_IMAGE_EXTENSIONS
        
        new_filename = sha256(file_content).hexdigest() + ext
        
        file_name = default_storage.save(new_filename, ContentFile(file_content))
        file_url = default_storage.url(file_name)
        
        Image.objects.get_or_create(filename=new_filename)
        
        return JsonResponse({'url': file_url})
    except RequestDataTooBig:
        return fast413
    except AssertionError:
        return fast422