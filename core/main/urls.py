# from django.conf import settings
# from django.contrib import admin
# from django.urls import path
from typing import List

from django.conf import settings
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from purchase_order.views import PurchaseOrderViewSet
from vendor.views import VendorViewSet

router = SimpleRouter()
router.register(r'vendors', VendorViewSet, basename='vendors')
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_orders')

urlpatterns: List[path] = [
    path(f'{settings.API_PREFIX}/', include(router.urls)),
]
