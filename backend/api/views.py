import rest_framework.request
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from notifications.signals import notify

from .messages import *
from .models import *
from .serializers import *


@swagger_auto_schema(method="get", responses={200: ItemSerializer(), 404: ITEM_NOT_FOUND})
@api_view(["GET"])
@permission_classes([AllowAny])
def get_item(_, item_id):
    try:
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return JsonResponse({"message": ITEM_NOT_FOUND}, status=404)


@swagger_auto_schema(method="get", responses={200: ItemSerializer(many=True)})
@api_view(["GET"])
@permission_classes([AllowAny])
def get_items(_):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method="get", responses={200: ItemSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_items(request: rest_framework.request.Request):
    items = request.user.item_set.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="物品名称"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="物品描述"),
        "contact_info": openapi.Schema(type=openapi.TYPE_STRING, description="联系人信息"),
    },
    required=["name", "description", "contact_info"],
)


@swagger_auto_schema(
    method="post",
    request_body=item_schema,
    responses={200: ItemSerializer(), 400: INVALID_REQUEST},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=200)
    return Response(INVALID_REQUEST, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user or request.user.is_staff:
            item.delete()
            return JsonResponse({"message": DELETE_SUCCESS})
        else:
            return JsonResponse({"message": PERMISSION_DENIED}, status=403)
    except Item.DoesNotExist:
        return JsonResponse({"message": ITEM_NOT_FOUND}, status=404)


@swagger_auto_schema(
    method="post",
    request_body=item_schema,
    responses={200: ItemSerializer()},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    assert type(request.data) == dict, type(request.data)
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user:
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return JsonResponse({"message": INVALID_REQUEST}, status=400)
        else:
            return JsonResponse({"message": PERMISSION_DENIED}, status=403)
    except Item.DoesNotExist:
        return JsonResponse({"message": ITEM_NOT_FOUND}, status=404)


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter("q", openapi.IN_QUERY, description="物品名称或描述", type=openapi.TYPE_STRING, required=False)],
    responses={200: ItemSerializer()},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def search_items(request: rest_framework.request.Request):
    query = request.GET.get("q")
    if not query:
        return get_items(request._request)
    items = Item.objects.filter(name__icontains=query) | Item.objects.filter(description__icontains=query)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method="get", responses={200: UserSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


@swagger_auto_schema(
    method="post",
    responses={200: RIVIVE_SUCCESS, 404: INVALID_REQUEST, 403: PERMISSION_DENIED},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_deal(request: rest_framework.request.Request, notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        if not notification.unread:
            return JsonResponse({"message": INVALID_REQUEST}, status=404)
        deal: Transaction = notification.action_object
        item = deal.target
        new_owner = deal.buyer
        if (new_owner != request.user and item.owner == request.user and request.user == notification.recipient) or request.user.is_staff:
            item.owner.balance += deal.price
            item.owner.save()
            item.owner = new_owner
            item.save()
            notification.mark_as_read()
            return JsonResponse({"message": RIVIVE_SUCCESS})
        else:
            return JsonResponse({"message": PERMISSION_DENIED}, status=403)
    except Notification.DoesNotExist:
        return JsonResponse({"message": INVALID_REQUEST}, status=404)


@swagger_auto_schema(
    method="post",
    responses={200: REJECT_SUCCESS, 404: INVALID_REQUEST, 403: PERMISSION_DENIED},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_deal(request: rest_framework.request.Request, notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        if not notification.unread:
            return JsonResponse({"message": INVALID_REQUEST}, status=404)
        if notification.recipient != request.user:
            return JsonResponse({"message": PERMISSION_DENIED}, status=403)
        deal: Transaction = notification.action_object
        buyer = deal.buyer
        buyer.balance += deal.price
        buyer.save()
        notification.mark_as_read()
        return JsonResponse({"message": REJECT_SUCCESS})
    except Notification.DoesNotExist:
        return JsonResponse({"message": INVALID_REQUEST}, status=404)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "price": openapi.Schema(type=openapi.TYPE_INTEGER, description="为了复活物品愿意消耗的功德"),
        },
        required=["price"],
    ),
    responses={200: PROPOSAL_SUBMITTED, 404: ITEM_NOT_FOUND, 403: NO_BALANCE, 400: INVALID_REQUEST},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revive(request: rest_framework.request.Request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        price = int(request.data.get("price"))
        buyer: User = request.user
        if not isinstance(price, int) or price < 0:
            return JsonResponse({"message": INVALID_REQUEST, "price": repr(price)}, status=400)
        if item.owner != buyer or buyer.is_staff:
            if buyer.balance >= price or buyer.is_staff:
                deal = Transaction.objects.create(buyer=buyer, target=item, price=price)
                buyer.balance -= price
                buyer.save()
                notify.send(request.user, verb="proposed", action_object=deal, recipient=item.owner)
                return JsonResponse({"message": PROPOSAL_SUBMITTED})
            else:
                return JsonResponse({"message": NO_BALANCE}, status=403)
        else:
            return JsonResponse({"message": INVALID_REVIVE}, status=403)
    except Item.DoesNotExist:
        return JsonResponse({"message": ITEM_NOT_FOUND}, status=404)


@swagger_auto_schema(method="get", responses={200: NotificationSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_notifications(request: rest_framework.request.Request):
    notifications = request.user.notifications.all()
    return Response(NotificationSerializer(notifications, many=True).data)
