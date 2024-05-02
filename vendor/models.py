import uuid

from django.db import models

# Create your models here.


class Vendor(models.Model):
    vid = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True)
    name = models.CharField(max_length=52, null=False, blank=False)
    contact_details = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    vendor_code = models.CharField(max_length=10, null=False, blank=False, unique=True)

    on_time_delivery_date = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    class Meta:
        db_table = 'vendor\".\"vendor_information'


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey("Vendor", null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    on_time_delivery_date = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    class Meta:
        db_table = 'vendor\".\"historical_performance'
