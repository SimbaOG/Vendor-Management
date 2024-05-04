from rest_framework.serializers import ModelSerializer

from vendor.models import Vendor


class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

        extra_kwargs = {'vid': {'read_only': True}}
