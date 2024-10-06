import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Item
from django.contrib.auth.models import User

class GetItemsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.item1 = Item.objects.create(name = 'Item 1', description = 'Description 1', contact_info = 'Contact 1', owner = self.user)
        self.item2 = Item.objects.create(name = 'Item 2', description = 'Description 2', contact_info = 'Contact 2', owner = self.user)


    def test_get_all_items(self):
        response = self.client.get(reverse('get_items'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_get_single_item(self):
        response = self.client.get(reverse('get_item', args = [
            self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Item 1')


    def test_get_nonexistent_item(self):
        response = self.client.get(reverse('get_item', args = [
            999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Item not found')



class AddItemTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.client.login(username = 'testuser', password = 'testpass')


    def test_add_item(self):
        data = {
            'name': 'New Item',
            'description': 'New Description',
            'contact_info': 'New Contact' }
        response = self.client.post(reverse('add_item'), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().name, 'New Item')


    def test_add_item_unauthenticated(self):
        self.client.logout()
        data = {
            'name': 'New Item',
            'description': 'New Description',
            'contact_info': 'New Contact' }
        response = self.client.post(reverse('add_item'), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 403)



class DeleteItemTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.item = Item.objects.create(name = 'Item 1', description = 'Description 1', contact_info = 'Contact 1', owner = self.user)
        self.client.login(username = 'testuser', password = 'testpass')


    def test_delete_item(self):
        response = self.client.post(reverse('delete_item', args = [
            self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)


    def test_delete_nonexistent_item(self):
        response = self.client.post(reverse('delete_item', args = [
            999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Item not found')


    def test_delete_item_unauthorized(self):
        self.client.logout()
        response = self.client.post(reverse('delete_item', args = [
            self.item.id]))
        self.assertEqual(response.status_code, 403)



class UpdateItemTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.item = Item.objects.create(name = 'Item 1', description = 'Description 1', contact_info = 'Contact 1', owner = self.user)
        self.client.login(username = 'testuser', password = 'testpass')


    def test_update_item(self):
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'contact_info': 'Updated Contact' }
        response = self.client.post(reverse('update_item', args = [
            self.item.id]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')


    def test_update_nonexistent_item(self):
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'contact_info': 'Updated Contact' }
        response = self.client.post(reverse('update_item', args = [
            999]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Item not found')


    def test_update_item_unauthorized(self):
        self.client.logout()
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'contact_info': 'Updated Contact' }
        response = self.client.post(reverse('update_item', args = [
            self.item.id]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 403)



class SearchItemsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.item1 = Item.objects.create(name = 'Item 1', description = 'Description 1', contact_info = 'Contact 1', owner = self.user)
        self.item2 = Item.objects.create(name = 'Item 2', description = 'Description 2', contact_info = 'Contact 2', owner = self.user)


    def test_search_items(self):
        response = self.client.get(reverse('search_items'), {
            'q': 'Item 1' })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Item 1')


    def test_search_items_no_query(self):
        response = self.client.get(reverse('search_items'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)



class GetUserInfoTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.client.login(username = 'testuser', password = 'testpass')


    def test_get_user_info(self):
        response = self.client.get(reverse('get_user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'testuser')


    def test_get_user_info_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('get_user_info'))
        self.assertEqual(response.status_code, 403)



class TransferOwnershipTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username = 'testuser1', password = 'testpass')
        self.user2 = User.objects.create_user(username = 'testuser2', password = 'testpass')
        self.item = Item.objects.create(name = 'Item 1', description = 'Description 1', contact_info = 'Contact 1', owner = self.user1)
        self.client.login(username = 'testuser1', password = 'testpass')


    def test_transfer_ownership(self):
        data = {
            'new_owner': 'testuser2' }
        response = self.client.post(reverse('transfer_ownership', args = [
            self.item.id]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.owner, self.user2)


    def test_transfer_ownership_nonexistent_item(self):
        data = {
            'new_owner': 'testuser2' }
        response = self.client.post(reverse('transfer_ownership', args = [
            999]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Item not found')


    def test_transfer_ownership_nonexistent_user(self):
        data = {
            'new_owner': 'nonexistentuser' }
        response = self.client.post(reverse('transfer_ownership', args = [
            self.item.id]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'New owner not found')


    def test_transfer_ownership_unauthorized(self):
        self.client.logout()
        data = {
            'new_owner': 'testuser2' }
        response = self.client.post(reverse('transfer_ownership', args = [
            self.item.id]), data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 403)


