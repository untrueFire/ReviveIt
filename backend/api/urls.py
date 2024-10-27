from django.urls import path

from .views import *

urlpatterns = [
    path("items/add/", add_item, name="add_item"),
    path("items/delete/<int:item_id>/", delete_item, name="delete_item"),
    path("items/<int:item_id>/", get_item, name="get_item"),
    path("items/revive/<int:item_id>/", revive, name="revive"),
    path("items/search/", search_items, name="search_items"),
    path("items/update/<int:item_id>/", update_item, name="update_item"),
    path("notification/accept/<int:notification_id>/", accept_deal, name="accept_deal"),
    path("notification/read/<int:notification_id>/", read, name="read"),
    path("notification/reject/<int:notification_id>/", reject_deal, name="reject_deal"),
    path("tag/add/", add_tag, name="add_tag"),
    path("tag/remove/", remove_tag, name="remove_tag"),
    path("tag/search/", search_tag, name="search_tag"),
    path("user/challenge/", challenge, name="challenge"),
    path("user/", get_user_info, name="get_user_info"),
    path("user/items/", get_my_items, name="get_my_items"),
    path("user/knock/", knock, name="knock"),
    path("user/notifications/read/", user_notifications_read, name="user_notifications_read"),
    path("user/notifications/unread/", user_notifications_unread, name="user_notifications_unread"),
    path("user/notifications/", user_notifications, name="user_notifications"),
]
