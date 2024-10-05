# items/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path("items/", get_items, name="get_items"),
    path("items/<int:item_id>/", get_item, name="get_item"),
    path("items/add/", add_item, name="add_item"),
    path("items/delete/<int:item_id>/", delete_item, name="delete_item"),
    path("items/update/<int:item_id>/", update_item, name="update_item"),
    path("items/transfer/<int:item_id>/", transfer_ownership, name="transfer_ownership"),
    path("search/", search_items, name="search_items"),
]
