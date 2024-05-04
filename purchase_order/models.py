from django.db import models

from purchase_order.utils.misc import generate_crpto_accurate_keys

# Create your models here.

STATUS_CHOICE = [
    ("pending", "pending"),
    ("completed", "completed"),
    ("cancelled", "cancelled"),
]


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=8, default=generate_crpto_accurate_keys, db_index=True, primary_key=True)
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE, null=False)
    order_date = models.DateTimeField(null=False)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=10, null=False, blank=False, choices=STATUS_CHOICE, default="pending")
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgement_date = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'vendor\".\"purchase_orders'
        constraints = [
            models.constraints.CheckConstraint(
                check=models.Q(quality_rating__gte=1, quality_rating__lte=10), name='quality_rating_range_constrained'
            )
        ]
