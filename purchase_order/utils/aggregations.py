from django.db import close_old_connections, connection
from django.db.models import Avg, Count, ExpressionWrapper, F, FloatField, Q
from django.db.models.functions import Cast

from purchase_order.models import PurchaseOrder
from vendor.models import HistoricalPerformance, Vendor


def handle_po_changes(
    po_object: PurchaseOrder,
    received_data: dict = None,
    delete_po: bool = False,
    acknowledge_po: bool = False
) -> None:
    """
    Function to handle changes in Purchase Order data and update Vendor data metrics accordingly.
    :param po_object:  Purchase Order object
    :param received_data: dict containing the data received from the request
    :param delete_po: True if the po has to be deleted
    :param acknowledge_po: True if po has to be acknowledged
    :return:
    """

    annotations_dictionary = {}

    all_vendor_pos = PurchaseOrder.objects.filter(vendor=po_object.vendor)

    on_time_delivery_rate_formula = ExpressionWrapper((
        Cast(Count('po_number', filter=Q(completed_at__lte=F('delivery_date'))), output_field=FloatField()) /
        Cast(Count('po_number'), output_field=FloatField())
    ) * 100,
                                                      output_field=FloatField())  # noqa: E126
    avg_quality_rating_formula = Avg('quality_rating')
    avg_resp_time_formula = Avg(F('acknowledgement_date') - F('issue_date'))
    fulfillment_rate_formula = ExpressionWrapper((
        Cast(Count('po_number', filter=Q(status='completed')), output_field=FloatField()) /
        Cast(Count('po_number'), output_field=FloatField())
    ) * 100,
                                                 output_field=FloatField())  # noqa: E126

    if delete_po:
        annotations_dictionary['on_time_delivery_rate'] = on_time_delivery_rate_formula
        annotations_dictionary['avg_quality_rating'] = avg_quality_rating_formula
        annotations_dictionary['avg_response_time'] = avg_resp_time_formula
        annotations_dictionary['fulfillment_rate'] = fulfillment_rate_formula
    elif acknowledge_po:
        annotations_dictionary['avg_response_time'] = avg_resp_time_formula
    elif isinstance(received_data, dict):
        if status := received_data.get('status', None):
            annotations_dictionary['fulfillment_rate'] = fulfillment_rate_formula
            if status == 'completed':
                # On-time delivery rate calculation
                annotations_dictionary['on_time_delivery_rate'] = on_time_delivery_rate_formula

                if received_data.get('quality_rating', None):
                    annotations_dictionary['avg_quality_rating'] = avg_quality_rating_formula
    else:
        return

    aggregated_data = all_vendor_pos.aggregate(**annotations_dictionary)

    if bool(aggregated_data):
        field_mapper = {
            'avg_quality_rating': 'quality_rating_avg',
            'on_time_delivery_rate': 'on_time_delivery_rate',
            'avg_response_time': 'average_response_time',
            'fulfillment_rate': 'fulfillment_rate',
        }
        update_fields = {}
        print(aggregated_data)
        for key, value in aggregated_data.items():
            if key == 'avg_response_time':
                update_fields[field_mapper[key]] = value.total_seconds()
            else:
                update_fields[field_mapper[key]] = value

        Vendor.objects.filter(vid=po_object.vendor_id).update(**update_fields)

    connection.close()
    close_old_connections()


def vendor_historical_performance_logger(vendor_id: str):
    vendor_current_data = list(
        Vendor.objects.filter(
            vid=vendor_id
        ).values('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    )
    if vendor_current_data:
        HistoricalPerformance.objects.create(vendor_id=vendor_id, **vendor_current_data[0])

    connection.close()
    close_old_connections()
