from django.urls import path

from .views import *

urlpatterns = [
    path("items/<int:item_id>/", get_item, name="get_item"),
    path("items/add/", add_item, name="add_item"),
    path("items/delete/<int:item_id>/", delete_item, name="delete_item"),
    path("items/update/<int:item_id>/", update_item, name="update_item"),
    path("notification/accept/<int:notification_id>/", accept_deal, name="accept_deal"),
    path("notification/reject/<int:notification_id>/", reject_deal, name="reject_deal"),
    path("notification/read/<int:notification_id>/", read, name="read"),
    path("items/revive/<int:item_id>/", revive, name="revive"),
    path("search/", search_items, name="search_items"),
    path("user/", get_user_info, name="get_user_info"),
    path("user/items/", get_my_items, name="get_my_items"),
    path("user/notifications/", user_notifications, name="user_notifications"),
    path("user/challenge/", challenge, name="challenge"),
    path("user/knock/", knock, name="knock"),
]
