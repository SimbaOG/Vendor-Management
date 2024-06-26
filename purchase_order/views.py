# from django.shortcuts import render
from datetime import datetime as dt
from zoneinfo import ZoneInfo

from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.core.utils.background_tasks import global_scheduler
from core.core.utils.misc import string_to_datetime

from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from .utils.aggregations import handle_po_changes, vendor_historical_performance_logger

# Create your views here.


class PurchaseOrderViewSet(ViewSet):
    """
    ViewSet for PurchaseOrder model
    """

    def list(self, request):  # noqa: A003
        """
        Function to list all the Purchase Orders
        :param request:
        :return:
        """

        purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)

        return Response(serializer.data)

    def create(self, request):
        """
        Function to create a new Purchase Order
        :param request:
        :return:
        """

        received_data = request.data

        received_data.pop('completed_at', None)
        received_data.pop('quality_rating', None)

        if (items := received_data.get('items')) and (quantity := received_data.get('quantity')):
            if len(items.keys()) != quantity:
                return Response({'detail': 'No. of items and quantity should match!'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'items and quantity, both should be present when raising a PO.'},
                            status=status.HTTP_400_BAD_REQUEST)

        delivery_date = string_to_datetime(received_data.get('delivery_date', None))
        order_date = string_to_datetime(received_data.get('order_date', None))

        if delivery_date and order_date:
            if delivery_date < order_date:
                return Response({'detail': 'Delivery date can not be before order date!'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = PurchaseOrderSerializer(data=received_data)
        if serializer.is_valid():
            global_scheduler.add_job(vendor_historical_performance_logger, 'date', [received_data['vendor']])
            instance = serializer.save()
            po_obj = PurchaseOrder.objects.get(po_number=instance.po_number)
            global_scheduler.add_job(handle_po_changes, 'date', [po_obj, received_data])
            return Response({'detail': 'PO raised successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'put', 'delete'], detail=False, url_path='(?P<po_id>[0-9A-Za-z]{8})')
    def handle_single_po(self, request, *args, **kwargs):  # noqa: C901
        """
        Function to handle a single Purchase Order
        It handles GET, PUT and DELETE requests, which are used to get, update and delete a Purchase Order
        respectively.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        po_id = self.kwargs['po_id']

        if request.method.casefold() == 'get':
            po_obj = get_object_or_404(PurchaseOrder, po_number=po_id)

            serializer = PurchaseOrderSerializer(po_obj)
            return Response(serializer.data)

        elif request.method.casefold() == 'delete':
            po_obj = get_object_or_404(PurchaseOrder, po_number=po_id)

            try:
                global_scheduler.add_job(vendor_historical_performance_logger, 'date', [po_obj.vendor_id])
                po_obj.delete()
                global_scheduler.add_job(handle_po_changes, 'date', [po_obj], {'delete_po': True})
            except IntegrityError:
                return Response({'detail': 'Failed to delete the purchase order.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': 'Purchase order deleted successfully!'}, status=status.HTTP_200_OK)

        elif request.method.casefold() == 'put':
            received_data = request.data

            received_data.pop('completed_at', None)
            quantity = received_data.get('quantity', None)
            items = received_data.get('items', None)

            po_obj = get_object_or_404(PurchaseOrder, po_number=po_id)

            if po_obj.status.casefold() == 'completed':
                return Response({'detail': 'PO has already been completed. Can not updated furthermore!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if quantity and items:
                if len(items.keys()) != quantity:
                    return Response({'detail': 'No. of items and quantity should match!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif quantity:
                if len(po_obj.items.keys()) != quantity:
                    return Response({'detail': 'No. of items and quantity should match!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif items:
                if len(items.keys) != po_obj.quantity:
                    return Response({'detail': 'No. of items and quantity should match!'},
                                    status=status.HTTP_400_BAD_REQUEST)

            if po_status := received_data.get('status'):
                if po_status.casefold() == 'completed':
                    received_data['completed_at'] = dt.now(tz=ZoneInfo('Asia/Kolkata'))

            delivery_date = string_to_datetime(received_data.get('delivery_date', None))
            order_date = string_to_datetime(received_data.get('order_date', None))

            if delivery_date and order_date:
                if delivery_date < order_date:
                    return Response({'detail': 'Delivery date can not be before order date!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif delivery_date:
                if po_obj.order_date and (delivery_date < po_obj.order_date):
                    return Response({'detail': 'Delivery date can not be before order date!'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif order_date:
                if po_obj.delivery_date and (delivery_date < po_obj.order_date):
                    return Response({'detail': 'Order date can not be after the delivery date!'},
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer = PurchaseOrderSerializer(po_obj, received_data, partial=True)
            if serializer.is_valid():
                global_scheduler.add_job(vendor_historical_performance_logger, 'date', [po_obj.vendor_id])
                serializer.save()
                global_scheduler.add_job(handle_po_changes, 'date', [po_obj, received_data])
                return Response({'detail': 'Purchase order updated successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='(?P<po_id>[0-9A-Za-z]{8})/acknowledge')
    def acknowledge_po(self, request, *args, **kwargs):
        """
        Function to acknowledge a Purchase Order.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        po_id = self.kwargs['po_id']

        po_obj = get_object_or_404(PurchaseOrder, po_number=po_id)

        if po_obj.acknowledgement_date:
            return Response({'detail': 'PO has already been acknowledged!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            global_scheduler.add_job(vendor_historical_performance_logger, 'date', [po_obj.vendor_id])
            po_obj.acknowledgement_date = dt.now(tz=ZoneInfo('Asia/Kolkata'))
            po_obj.save(update_fields=['acknowledgement_date'])
            global_scheduler.add_job(handle_po_changes, 'date', [po_obj], {'acknowledge_po': True})
            return Response({'detail': 'PO acknowledged successfully!'}, status=status.HTTP_200_OK)
