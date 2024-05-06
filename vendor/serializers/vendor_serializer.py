from rest_framework.serializers import ModelSerializer, SerializerMethodField

from vendor.models import Vendor


class VendorSerializer(ModelSerializer):
    """
    Serializer for Vendor model
    """

    class Meta:
        model = Vendor
        exclude = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

        extra_kwargs = {'vid': {'read_only': True}}


class VendorPerformanceSerializer(ModelSerializer):
    """
    Serializer for Vendor model with performance metrics
    """

    average_response_time = SerializerMethodField('convert_resp_time')

    class Meta:
        model = Vendor
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

    def convert_resp_time(self, obj):
        """
        Convert average response time to HH:MM:SS format
        :param obj:
        :return:
        """
        total_seconds = obj.average_response_time
        if isinstance(total_seconds, float):
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f'{int(hours)}:{int(minutes)}:{int(seconds)}'
        return None
