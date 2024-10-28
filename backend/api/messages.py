from django.http import JsonResponse
from rest_framework import status

SUCCESS = "请求成功"
NOT_FOUND = "未找到"
PERMISSION_DENIED = "权限不足"
INVALID_REQUEST = "无效请求"
NO_CRED = "未登录"
NO_BALANCE = "功德不足"
REJECT_SUCCESS = "拒绝成功"
REQUEST_TOO_BIG = "文件过大"
NO_FILE = "未提供文件"
INVALID_FORMAT = "不支持的格式"

fast200 = JsonResponse({"message": SUCCESS})
fast400 = JsonResponse({"message": INVALID_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
fast403 = JsonResponse({"message": PERMISSION_DENIED}, status=status.HTTP_403_FORBIDDEN)
fast404 = JsonResponse({"message": NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
fast413 = JsonResponse({"error": REQUEST_TOO_BIG}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
fast422 = JsonResponse({"err": INVALID_FORMAT}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
