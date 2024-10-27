from django.http import JsonResponse

SUCCESS = "请求成功"
NOT_FOUND = "未找到"
PERMISSION_DENIED = "权限不足"
INVALID_REQUEST = "无效请求"
NO_CRED = "未登录"
NO_BALANCE = "功德不足"
REJECT_SUCCESS = "拒绝成功"

fast200 = JsonResponse({"message": SUCCESS})
fast400 = JsonResponse({"message": INVALID_REQUEST}, status=400)
fast403 = JsonResponse({"message": PERMISSION_DENIED}, status=403)
fast404 = JsonResponse({"message": NOT_FOUND}, status=404)
