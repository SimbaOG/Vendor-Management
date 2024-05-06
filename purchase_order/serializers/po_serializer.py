from rest_framework.serializers import ModelSerializer

from ..models import PurchaseOrder


class PurchaseOrderSerializer(ModelSerializer):
    """
    Serializer for PurchaseOrder model
    """

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

        extra_kwargs = {'issue_date': {'read_only': True}, 'po_number': {'read_only': True}}
