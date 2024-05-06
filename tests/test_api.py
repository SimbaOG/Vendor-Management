from rest_framework.test import APITestCase

from accounts.models import Account
from purchase_order.models import PurchaseOrder
from vendor.models import Vendor


class TestApiEndpoints(APITestCase):
    """
    Test cases for the API endpoints
    """

    def setUp(self):
        user, _ = Account.objects.get_or_create(email="test@gmail.com", password="test123")
        self.client.force_authenticate(user=user)

    def create_account(self, email="test@gmail.com", password="test123"):
        return Account.objects.create_user(email=email, password=password)

    def test_account_login(self):
        self.create_account()
        response = self.client.post('/api/accounts/login/', {'email': 'test@gmail.com', 'password': 'test123'})
        fail_response = self.client.post('/api/accounts/login/', {'email': '', 'password': ''})
        invalid_response = self.client.post('/api/accounts/login/', {'email': 'test@gmail.com', 'password': 't1234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertEqual(fail_response.status_code, 404)
        self.assertEqual(invalid_response.status_code, 400)

    def test_account_creation(self):
        response = self.client.post('/api/accounts/', {'email': 'test2@gmail.com', 'password': 'test123'})
        self.assertEqual(response.status_code, 201)

    def create_vendor(self, name="test", contact_details="test", address="test", vendor_code="test"):
        return Vendor.objects.create(
            name=name, contact_details=contact_details, address=address, vendor_code=vendor_code
        )

    def test_vendor_creation(self):
        response = self.client.post(
            '/api/vendors/', {
                'name': 'test',
                'contact_details': 'test',
                'address': 'test',
                'vendor_code': 'test'
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'test')
        self.assertEqual(Vendor.objects.get().contact_details, 'test')
        self.assertEqual(Vendor.objects.get().address, 'test')
        self.assertEqual(Vendor.objects.get().vendor_code, 'test')
        self.assertEqual(Vendor.objects.get().on_time_delivery_rate, None)
        self.assertEqual(Vendor.objects.get().quality_rating_avg, None)
        self.assertEqual(Vendor.objects.get().average_response_time, None)
        self.assertEqual(Vendor.objects.get().fulfillment_rate, None)

    def test_vendor_creation_with_invalid_data(self):
        response = self.client.post('/api/vendors/', {'name': 'test', 'contact_details': 'test', 'address': 'test'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_creation_with_duplicate_vendor_code(self):
        self.create_vendor()
        response = self.client.post(
            '/api/vendors/', {
                'name': 'test',
                'contact_details': 'test',
                'address': 'test',
                'vendor_code': 'test'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_vendor_listing(self):
        self.create_vendor()
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'test')
        self.assertEqual(response.data[0]['contact_details'], 'test')
        self.assertEqual(response.data[0]['address'], 'test')
        self.assertEqual(response.data[0]['vendor_code'], 'test')

    def test_vendor_listing_with_no_vendors(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_single_vendor(self):
        vendor = self.create_vendor()
        response = self.client.get(f'/api/vendors/{vendor.vid}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['contact_details'], 'test')
        self.assertEqual(response.data['address'], 'test')
        self.assertEqual(response.data['vendor_code'], 'test')

    def test_single_vendor_with_invalid_id(self):
        response = self.client.get('/api/vendors/123/')
        self.assertEqual(response.status_code, 404)

    def test_delete_single_vendor(self):
        vendor = self.create_vendor()
        response = self.client.delete(f'/api/vendors/{vendor.vid}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_delete_single_vendor_with_invalid_id(self):
        response = self.client.delete('/api/vendors/123/')
        self.assertEqual(response.status_code, 404)

    def test_update_single_vendor(self):
        vendor = self.create_vendor()
        response = self.client.put(
            f'/api/vendors/{vendor.vid}/', {
                'name': 'test1',
                'contact_details': 'test1',
                'address': 'test1',
                'vendor_code': 'test1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.get().name, 'test1')
        self.assertEqual(Vendor.objects.get().contact_details, 'test1')
        self.assertEqual(Vendor.objects.get().address, 'test1')
        self.assertEqual(Vendor.objects.get().vendor_code, 'test1')

    def test_update_single_vendor_with_invalid_data(self):
        response = self.client.put(
            '/api/vendors/123/', {
                'name': 'test1',
                'contact_details': '12345678',
                'address': 'test1'
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_update_single_vendor_with_duplicate_vendor_code(self):
        vendor1 = self.create_vendor()
        vendor2 = self.create_vendor(name='test1', contact_details='test1', address='test1', vendor_code='test1')
        response = self.client.put(
            f'/api/vendors/{vendor1.vid}/', {
                'name': 'test1',
                'contact_details': 'test1',
                'address': 'test1',
                'vendor_code': 'test1'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Vendor.objects.count(), 2)
        self.assertEqual(Vendor.objects.get(vid=vendor1.vid).name, 'test')
        self.assertEqual(Vendor.objects.get(vid=vendor2.vid).name, 'test1')
        self.assertEqual(Vendor.objects.get(vid=vendor1.vid).vendor_code, 'test')
        self.assertEqual(Vendor.objects.get(vid=vendor2.vid).vendor_code, 'test1')

    def test_update_vendor_with_no_data(self):
        vendor = self.create_vendor()
        response = self.client.put(f'/api/vendors/{vendor.vid}/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vendor.objects.get().name, 'test')
        self.assertEqual(Vendor.objects.get().contact_details, 'test')
        self.assertEqual(Vendor.objects.get().address, 'test')
        self.assertEqual(Vendor.objects.get().vendor_code, 'test')

    def test_vendor_performance(self):
        vendor = self.create_vendor()
        response = self.client.get(f'/api/vendors/{vendor.vid}/performance/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['on_time_delivery_rate'], None)
        self.assertEqual(response.data['quality_rating_avg'], None)
        self.assertEqual(response.data['average_response_time'], None)
        self.assertEqual(response.data['fulfillment_rate'], None)

    def test_vendor_performance_with_invalid_id(self):
        response = self.client.get('/api/vendors/123/performance/')
        self.assertEqual(response.status_code, 404)

    def create_purchase_order(
        self,
        vendor,
        order_date="2024-05-02T22:00:00+05:30",
        delivery_date="2024-05-02T22:00:00+05:30",
        status="pending"
    ):
        items = {'food': 'yum'}
        quantity = 1
        return PurchaseOrder.objects.create(
            vendor=vendor,
            order_date=order_date,
            delivery_date=delivery_date,
            status=status,
            items=items,
            quantity=quantity
        )

    def test_purchase_order_creation(self):
        vendor = self.create_vendor()
        response = self.client.post(
            '/api/purchase_orders/', {
                'vendor': vendor.vid,
                'order_date': '2024-05-02T22:00:00+05:30',
                'delivery_date': '2024-05-02T22:00:00+05:30',
                'status': 'pending',
                'items': {
                    'food': 'yum'
                },
                'quantity': 1
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().vendor, vendor)
        self.assertEqual(PurchaseOrder.objects.get().status, 'pending')
        self.assertEqual(PurchaseOrder.objects.get().items, {'food': 'yum'})
        self.assertEqual(PurchaseOrder.objects.get().quantity, 1)

    def test_purchase_order_creation_with_invalid_data(self):
        response = self.client.post(
            '/api/purchase_orders/', {
                'vendor': '123',
                'order_date': '2024-05-02T22:00:00+05:30',
                'delivery_date': '2024-05-02T22:00:00+05:30',
                'status': 'pending',
                'items': {
                    'food': 'yum'
                },
                'quantity': 1
            },
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_purchase_order_listing(self):
        vendor = self.create_vendor()
        self.create_purchase_order(vendor)
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(response.data[0]['vendor']), str(vendor.vid))
        self.assertEqual(response.data[0]['status'], 'pending')
        self.assertEqual(response.data[0]['items'], {'food': 'yum'})
        self.assertEqual(response.data[0]['quantity'], 1)

    def test_purchase_order_listing_with_no_purchase_orders(self):
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_single_purchase_order(self):
        vendor = self.create_vendor()
        purchase_order = self.create_purchase_order(vendor)
        response = self.client.get(f'/api/purchase_orders/{purchase_order.po_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data['vendor']), str(vendor.vid))
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['items'], {'food': 'yum'})
        self.assertEqual(response.data['quantity'], 1)

    def test_single_purchase_order_with_invalid_id(self):
        response = self.client.get('/api/purchase_orders/123/')
        self.assertEqual(response.status_code, 404)

    def test_delete_single_purchase_order(self):
        vendor = self.create_vendor()
        purchase_order = self.create_purchase_order(vendor)
        response = self.client.delete(f'/api/purchase_orders/{purchase_order.po_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_delete_single_purchase_order_with_invalid_id(self):
        response = self.client.delete('/api/purchase_orders/123/')
        self.assertEqual(response.status_code, 404)

    def test_update_single_purchase_order(self):
        vendor = self.create_vendor()
        purchase_order = self.create_purchase_order(vendor)
        response = self.client.put(
            f'/api/purchase_orders/{purchase_order.po_number}/', {
                'vendor': vendor.vid,
                'order_date': '2024-05-02T22:00:00+05:30',
                'delivery_date': '2024-05-02T22:00:00+05:30',
                'status': 'completed',
                'items': {
                    'food': 'yum'
                },
                'quantity': 1
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PurchaseOrder.objects.get().status, 'completed')
        self.assertEqual(PurchaseOrder.objects.get().items, {'food': 'yum'})
        self.assertEqual(PurchaseOrder.objects.get().quantity, 1)
