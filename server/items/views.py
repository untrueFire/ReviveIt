import rest_framework.request
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer, UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .messages import *


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


item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Item name"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Item description"),
        "contact_info": openapi.Schema(type=openapi.TYPE_STRING, description="Contact information"),
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
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user or request.user.is_staff:
            item.delete()
            return JsonResponse({"message": "Item deleted successfully"})
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
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user:
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        else:
            return Response({"message": PERMISSION_DENIED}, status=403)
    except Item.DoesNotExist:
        return Response({"message": ITEM_NOT_FOUND}, status=404)


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("q", openapi.IN_QUERY, description="Name or description of the item", type=openapi.TYPE_STRING, required=False)
    ],
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
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "new_owner": openapi.Schema(type=openapi.TYPE_STRING, description="Username of the new owner"),
        },
        required=["new_owner"],
    ),
    responses={200: "Ownership transferred successfully", 404: " or ".join([ITEM_NOT_FOUND, NEW_OWNER_NOT_FOUND]), 403: PERMISSION_DENIED},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer_ownership(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if item.owner == request.user or request.user.is_staff:
            new_owner_username = request.data.get("new_owner")
            try:
                new_owner = User.objects.get(username=new_owner_username)
                item.owner = new_owner
                item.save()
                return JsonResponse({"message": "Ownership transferred successfully"})
            except User.DoesNotExist:
                return JsonResponse({"message": NEW_OWNER_NOT_FOUND}, status=404)
        else:
            return JsonResponse({"message": PERMISSION_DENIED}, status=403)
    except Item.DoesNotExist:
        return JsonResponse({"message": ITEM_NOT_FOUND}, status=404)
