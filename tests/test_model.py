from django.test import TestCase

from accounts.models import Account, TokenManager
from purchase_order.models import PurchaseOrder
from vendor.models import HistoricalPerformance, Vendor


class TestModels(TestCase):
    """
    Test all the models in the application
    """

    def create_account(self, email="test@gmail.com", password="test123"):
        return Account.objects.create_user(email=email, password=password)

    def test_account(self):
        account = self.create_account()
        self.assertEqual(isinstance(account, Account), True)

    def create_token(self):
        account = self.create_account()
        return TokenManager.objects.create(user=account)

    def test_token(self):
        token = self.create_token()
        self.assertEqual(isinstance(token, TokenManager), True)

    def create_vendor(self, name="test", contact_details="test", address="test", vendor_code="test"):
        return Vendor.objects.create(
            name=name, contact_details=contact_details, address=address, vendor_code=vendor_code
        )

    def test_vendor(self):
        vendor = self.create_vendor()
        self.assertEqual(isinstance(vendor, Vendor), True)

    def create_historical_performance(
        self,
        vendor,
        on_time_delivery_rate=0.0,
        quality_rating_avg=0.0,
        average_response_time=0.0,
        fulfillment_rate=0.0
    ):
        return HistoricalPerformance.objects.create(
            vendor=vendor,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )

    def test_historical_performance(self):
        vendor = self.create_vendor()
        historical_performance = self.create_historical_performance(vendor)
        self.assertEqual(isinstance(historical_performance, HistoricalPerformance), True)

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

    def test_purchase_order(self):
        vendor = self.create_vendor()
        purchase_order = self.create_purchase_order(vendor)
        self.assertEqual(isinstance(purchase_order, PurchaseOrder), True)
