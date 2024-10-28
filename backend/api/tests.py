import json

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from notifications.models import Notification
from rest_framework import status
from rest_framework.test import APIClient

from .messages import *
from .models import *
from .serializers import *


class GetItemsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.item1 = Item.objects.create(name="Item 1", description="Description 1", contactInfo="Contact 1", owner=self.user)
        self.item2 = Item.objects.create(name="Item 2", description="Description 2", contactInfo="Contact 2", owner=self.user)

    def test_get_single_item(self):
        response = self.client.get(reverse("get_item", args=[self.item1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Item 1")

    def test_get_nonexistent_item(self):
        response = self.client.get(reverse("get_item", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], NOT_FOUND)


class AddItemTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_add_item_success(self):
        data = {"name": "New Item", "description": "New Description", "contactInfo": "New Contact"}
        response = self.client.post(reverse("add_item"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], SUCCESS)

    def test_add_item_unauthenticated(self):
        self.client.logout()
        data = {"name": "New Item", "description": "New Description", "contactInfo": "New Contact"}
        response = self.client.post(reverse("add_item"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_item_invalid(self):
        self.client.login(username="testuser", password="testpass")
        data = {"name": "New Item", "description": 1, "contactInfo": ""}
        response = self.client.post(reverse("add_item"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteItemTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2")
        self.item = Item.objects.create(name="Item 1", description="Description 1", contactInfo="Contact 1", owner=self.user)
        self.client.login(username="testuser", password="testpass")

    def test_delete_item(self):
        response = self.client.post(reverse("delete_item", args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_nonexistent_item(self):
        response = self.client.post(reverse("delete_item", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], NOT_FOUND)

    def test_delete_item_unauthorized(self):
        self.client.logout()
        response = self.client.post(reverse("delete_item", args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username="testuser2", password="testpass2")
        response = self.client.post(reverse("delete_item", args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateItemTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.item = Item.objects.create(name="Item 1", description="Description 1", contactInfo="Contact 1", owner=self.user)
        self.client.login(username="testuser", password="testpass")

    def test_update_item(self):
        data = {"name": "Updated Item"}
        response = self.client.post(reverse("update_item", args=[self.item.id]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, data["name"])

    def test_update_nonexistent_item(self):
        data = {"name": "Updated Item", "description": "Updated Description", "contactInfo": "Updated Contact"}
        response = self.client.post(reverse("update_item", args=[999]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], NOT_FOUND)

    def test_update_item_unauthorized(self):
        self.client.logout()
        data = {"name": "Updated Item", "description": "Updated Description", "contactInfo": "Updated Contact"}
        response = self.client.post(reverse("update_item", args=[self.item.id]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_invalid_data(self):
        data = {"name": False}
        response = self.client.post(reverse("update_item", args=[self.item.id]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], INVALID_REQUEST)

    def test_update_item_not_owner(self):
        User.objects.create_user(username="anotheruser", password="anotherpass")
        self.client.login(username="anotheruser", password="anotherpass")
        data = {"name": "Updated Item", "description": "Updated Description", "contactInfo": "Updated Contact"}
        response = self.client.post(reverse("update_item", args=[self.item.id]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["message"], PERMISSION_DENIED)


class SearchItemsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.item1 = Item.objects.create(name="Item 1", description="Description 1", contactInfo="Contact 1", owner=self.user)
        self.item2 = Item.objects.create(name="Item 2", description="Description 2", contactInfo="Contact 2", owner=self.user)

    def test_search_items(self):
        response = self.client.get(reverse("search_items"), {"q": "Item 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "Item 1")

        response = self.client.get(reverse("search_items"), {"q": "", "orderby": "-name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], "Item 2")

    def test_search_items_no_query(self):
        response = self.client.get(reverse("search_items"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


class GetUserInfoTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_get_user_info(self):
        response = self.client.get(reverse("get_user_info"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "testuser")

    def test_get_user_info_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("get_user_info"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AcceptDealTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.new_owner = User.objects.create_user(username="newowner", password="newpass")
        self.item = Item.objects.create(owner=self.user)
        self.transaction = Transaction.objects.create(buyer=self.new_owner, target=self.item, price=100)
        self.notification = Notification.objects.create(actor=self.new_owner, verb="proposed", action_object=self.transaction, recipient=self.user)
        self.notification2 = Notification.objects.create(actor=self.new_owner, verb="proposed", action_object=self.transaction, recipient=self.user)

    def test_accept_deal_success(self):
        self.client.login(username="testuser", password="testpass")
        balance = self.user.balance
        deal: Transaction = self.notification.action_object
        response = self.client.post(reverse("accept_deal", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.item.owner, self.new_owner)
        self.assertEqual(self.user.balance, balance + deal.price)

        response = self.client.post(reverse("accept_deal", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(reverse("accept_deal", args=[self.notification2.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.notification2.refresh_from_db()
        self.assertEqual(self.notification2.data, "sold out")

    def test_accept_deal_permission_denied(self):
        self.client.login(username="newowner", password="newpass")
        response = self.client.post(reverse("accept_deal", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_deal_invalid_request(self):
        self.client.login(username="newowner", password="newpass")
        response = self.client.post(reverse("accept_deal", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RejectDealTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.buyer = User.objects.create_user(username="buyer", password="buyerpass")
        self.client.login(username="testuser", password="testpass")
        self.item = Item.objects.create(owner=self.user)
        self.price = 50
        self.deal = Transaction.objects.create(buyer=self.buyer, target=self.item, price=self.price)
        self.notification = Notification.objects.create(action_object=self.deal, verb="proposed", unread=True, actor=self.buyer, recipient=self.user)

    def test_reject_deal_success(self):
        balance = self.buyer.balance
        response = self.client.post(reverse("reject_deal", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], SUCCESS)
        self.buyer.refresh_from_db()
        self.assertEqual(self.buyer.balance, balance + self.price)
        self.notification.refresh_from_db()
        self.assertFalse(self.notification.unread)

    def test_reject_deal_nonexistent_notification(self):
        response = self.client.post(reverse("reject_deal", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], NOT_FOUND)

    def test_reject_deal_already_read_notification(self):
        self.notification.unread = False
        self.notification.save()

        response = self.client.post(reverse("reject_deal", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], INVALID_REQUEST)

    def test_reject_deal_unauthorized(self):
        self.client.login(username="buyer", password="buyerpass")
        response = self.client.post(reverse("reject_deal", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["message"], PERMISSION_DENIED)


class ReviveTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass", balance=100)
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2")
        self.item = Item.objects.create(owner=self.user2)

    def test_revive_success(self):
        self.client.login(username="testuser", password="testpass")
        balance = self.user.balance
        price = 50
        response = self.client.post(reverse("revive", args=[self.item.id]), {"price": price})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, balance - price)

    def test_revive_item_not_found(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("revive", args=[999]), {"price": 50})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_revive_no_balance(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("revive", args=[self.item.id]), {"price": 1000})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revive_invalid_request(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("revive", args=[self.item.id]), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse("revive", args=[self.item.id]), {"price": -10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_revive_self(self):
        self.client.login(username="testuser2", password="testpass2")
        response = self.client.post(reverse("revive", args=[self.item.id]), {"price": 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserNotificationsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.notification = Notification.objects.create(actor=self.user, recipient=self.user)

    def test_user_notifications_success(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("user_notifications"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_user_notifications_unread(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("user_notifications_unread"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_user_notifications_read(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("user_notifications_read"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
        self.notification.mark_as_read()
        response = self.client.get(reverse("user_notifications_read"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_user_notifications_unauthenticated(self):
        response = self.client.get(reverse("user_notifications"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetMyItemTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2")
        self.item2 = Item.objects.create(name="Item 2", description="Description 2", contactInfo="Contact 2", owner=self.user2)

    def test_get_my_items_success(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("get_my_items"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

        self.item1 = Item.objects.create(name="Item 1", description="Description 1", contactInfo="Contact 1", owner=self.user)
        response = self.client.get(reverse("get_my_items"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], ItemSerializer(self.item1).data)

        self.item3 = Item.objects.create(name="Item 3", description="Description 3", contactInfo="Contact 3", owner=self.user)
        response = self.client.get(reverse("get_my_items"), QUERY_STRING="orderby=-name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0], ItemSerializer(self.item3).data)

    def test_get_my_items_unauthenticated(self):
        response = self.client.get(reverse("get_my_items"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")
        self.notification = Notification.objects.create(actor=self.other_user, recipient=self.user)

    def test_read_notification_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("read", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertFalse(self.notification.unread)

    def test_read_notification_unauthorized(self):
        self.client.logout()
        response = self.client.post(reverse("read", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_notification_not_found(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("read", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_notification_not_recipient(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse("read", args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChallengeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()

    def test_challenge_success(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("challenge"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("challenge", response.json())
        self.assertIn("difficulty", response.json())

    def test_challenge_unauthorized(self):
        response = self.client.post(reverse("challenge"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class KnockViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("challenge")).json()
        self.challenge = response["challenge"]
        self.difficulty = response["difficulty"]

    def test_knock_success(self):
        nonce = self.generate_valid_nonce(self.challenge, self.difficulty)
        data = {"nonce": nonce}
        response = self.client.post(reverse("knock"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 1)

    def test_knock_unauthorized(self):
        self.client.logout()
        data = {"nonce": "invalid_nonce"}
        response = self.client.post(reverse("knock"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_knock_no_challenge(self):
        self.client.login(username="testuser2", password="testpassword2")
        data = {"nonce": "invalid_nonce"}
        response = self.client.post(reverse("knock"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_knock_invalid_nonce(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"nonce": "invalid_nonce"}
        response = self.client.post(reverse("knock"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def generate_valid_nonce(self, challenge, difficulty):
        from hashlib import sha256
        from random import choices
        from string import ascii_letters

        while True:
            nonce = "".join(choices(ascii_letters, k=16))
            if sha256((challenge + nonce).encode()).hexdigest().endswith("0" * difficulty):
                return nonce


class TestTagViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)
        self.item = Item.objects.create(owner=self.user, name="Test Item")

    def test_add_tag(self):
        url = reverse("add_tag")
        data = {"item_id": self.item.id, "tags": ["tag1", "tag2"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertIn("tag1", self.item.tags.names())
        self.assertIn("tag2", self.item.tags.names())

    def test_add_tag_string(self):
        url = reverse("add_tag")
        data = {"item_id": self.item.id, "tags": "tag_string"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertIn("tag_string", self.item.tags.names())

    def test_add_tag_invalid_request(self):
        url = reverse("add_tag")
        data = {"item_id": self.item.id, "tags": 123}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_tag_permission_denied(self):
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        other_item = Item.objects.create(owner=other_user, name="Other Item")
        url = reverse("add_tag")
        data = {"item_id": other_item.id, "tags": ["tag1", "tag2"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_tag_not_found(self):
        url = reverse("add_tag")
        data = {"item_id": 9999, "tags": ["tag1", "tag2"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_tag(self):
        self.item.tags.add("tag1", "tag2")
        url = reverse("remove_tag")
        data = {"item_id": self.item.id, "tags": ["tag1"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertNotIn("tag1", self.item.tags.names())
        self.assertIn("tag2", self.item.tags.names())

    def test_remove_tag_string(self):
        self.item.tags.add("tag_string")
        url = reverse("remove_tag")
        data = {"item_id": self.item.id, "tags": "tag_string"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertNotIn("tag_string", self.item.tags.names())

    def test_remove_tag_invalid_request(self):
        url = reverse("remove_tag")
        data = {"item_id": self.item.id, "tags": 123}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_tag_permission_denied(self):
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        other_item = Item.objects.create(owner=other_user, name="Other Item")
        other_item.tags.add("tag1", "tag2")
        url = reverse("remove_tag")
        data = {"item_id": other_item.id, "tags": ["tag1"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_tag_not_found(self):
        url = reverse("remove_tag")
        data = {"item_id": 9999, "tags": ["tag1"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestMiddleware(TestCase):
    def setUp(self):
        pass

    def test_not_in_test(self):
        """
        To cover `if not is_test_environment():` in `./middleware.py`
        """
        import sys

        sys.argv[1:2] = [""]
        ReviveTestCase(methodName="test_revive_invalid_request").run()
        sys.argv[1:2] = ["test"]


class TestSearchTags(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="1", password="1")
        self.item1 = Item.objects.create(name="Item 1", description="desc1", contactInfo="contact1")
        self.item1.tags.add("tag2", "tag3")
        self.item2 = Item.objects.create(name="Item 2", description="desc2", contactInfo="contact2")
        self.item2.tags.add("tag1", "tag3")
        self.item3 = Item.objects.create(name="Item 3", description="desc3", contactInfo="contact3")
        self.item3.tags.add("tag1", "tag2")

    def test_search_tag_valid_request(self):
        url = reverse("search_tag")
        data = {"tags": ["tag1"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ItemSerializer([self.item2, self.item3], many=True).data
        self.assertEqual(response.json(), expected_data)

        data = {"tags": "tag2"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ItemSerializer([self.item1, self.item3], many=True).data
        self.assertEqual(response.json(), expected_data)

    def test_search_tag_invalid_request(self):
        url = reverse("search_tag")
        data = {}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_tag_pagination(self):
        url = reverse("search_tag")
        data = {"tags": ["tag3"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json", QUERY_STRING="limit=1&offset=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ItemSerializer([self.item2], many=True).data
        self.assertEqual(response.json(), expected_data)

    def test_search_tag_ordering(self):
        url = reverse("search_tag")
        data = {"tags": ["tag2"]}
        response = self.client.post(url, json.dumps(data), content_type="application/json", QUERY_STRING="orderby=-name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ItemSerializer([self.item3, self.item1], many=True).data
        self.assertEqual(response.json(), expected_data)


class UploadFileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('upload_file')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(self.user)
        self.uploaded_files = []  # 用于记录上传的文件名

    def test_upload_file_success(self):
        file_content = b'GIF89a'
        file_name = 'test_file.gif'
        file = SimpleUploadedFile(file_name, file_content)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('url', response_data)
        saved_file_name = response_data['url'].split('/')[-1]
        self.assertTrue(default_storage.exists(saved_file_name))
        self.uploaded_files.append(saved_file_name)

    def test_upload_file_no_file_provided(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], NO_FILE)

    def test_upload_file_too_big(self):
        file_content = b'a' * (settings.DATA_UPLOAD_MAX_MEMORY_SIZE + 1)
        file_name = 'large_file.png'
        file = SimpleUploadedFile(file_name, file_content)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

    def test_upload_file_invalid_type(self):
        file_content = b'<script>alert(1);</script>'
        file_name = 'bad_file.html'
        file = SimpleUploadedFile(file_name, file_content)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def tearDown(self):
        for file_name in self.uploaded_files:
            default_storage.delete(file_name)