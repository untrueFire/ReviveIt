from django.http import JsonResponse


SUCCCESS = "请求成功"
ITEM_NOT_FOUND = "未找到物品"
NEW_OWNER_NOT_FOUND = "复活者不存在"
PERMISSION_DENIED = "权限不足"
INVALID_REQUEST = "无效请求"
NO_CRED = "未登录"
DELETE_SUCCESS = "删除成功"
RIVIVE_SUCCESS = "交易成功"
INVALID_REVIVE = "不能复活自己的物品"
PROPOSAL_SUBMITTED = "成功提交复活申请"
NO_BALANCE = "功德不足"
REJECT_SUCCESS = "拒绝成功"

fast200 = JsonResponse({"message": SUCCCESS})
fast400 = JsonResponse({"message": INVALID_REQUEST}, status=400)
fast403 = JsonResponse({"message": PERMISSION_DENIED}, status=403)
fast404 = JsonResponse({"message": ITEM_NOT_FOUND}, status=404)