# from django.shortcuts import render
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from vendor.models import Vendor

from .serializers import VendorPerformanceSerializer, VendorSerializer

# Create your views here.


class VendorViewSet(GenericViewSet):
    """
    VendorViewSet class is a viewset class that handles all the API requests related to the Vendor model.
    """

    def list(self, request):  # noqa: A003
        """
        This method is used to list all the vendors in the database.
        :param request:
        :return:
        """
        vendor_objs = Vendor.objects.all()

        serializer = VendorSerializer(vendor_objs, many=True)

        return Response(serializer.data)

    def create(self, request):
        """
        This method is used to create a new vendor in the database.
        :param request:
        :return:
        """

        received_data = request.data
        serializer = VendorSerializer(data=received_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Vendor created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get', 'put', 'delete'],
        detail=False,
        url_path='(?P<vid>[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})'
    )
    def handle_single_vendor(self, request, *args, **kwargs):
        """
        This method is used to handle the requests related to a single vendor.
        It can handle GET, PUT and DELETE requests. Which are used to get, update and delete a vendor respectively.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        vendor_id = self.kwargs['vid']

        if request.method.casefold() == 'delete':

            vendor_obj = get_object_or_404(Vendor, vid=vendor_id)
            try:
                vendor_obj.delete()
            except IntegrityError:
                return Response({'detail': 'Unable to delete vendor as it is referenced elsewhere!'})

            return Response({'detail': 'Vendor deleted successfully!'})

        elif request.method.casefold() == 'get':

            vendor_obj = get_object_or_404(Vendor, vid=vendor_id)

            serializer = VendorSerializer(vendor_obj)

            return Response(serializer.data)

        elif request.method.casefold() == 'put':

            vendor_obj = get_object_or_404(Vendor, vid=vendor_id)
            received_data = request.data

            serializer = VendorSerializer(vendor_obj, received_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Vendor updated successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        url_path='(?P<vid>[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/performance'
    )
    def get_vendor_performance(self, request, *args, **kwargs):
        """
        This method is used to get the performance of a vendor.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        vendor_id = self.kwargs['vid']

        vendor_obj = get_object_or_404(Vendor, vid=vendor_id)

        serializer = VendorPerformanceSerializer(vendor_obj)
        return Response(serializer.data)
