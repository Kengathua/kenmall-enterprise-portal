from rest_framework import serializers
from kenmall_enterprise_portal.credit.models import (
    Purchase, PurchaseOrder, PurchaseOrderItem)
from kenmall_enterprise_portal.common.serializers import BaseSerializerMixin

class PurchaseOrderSerializer(BaseSerializerMixin):
    """Purchases order serializer."""

    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for purchases order serialiser"""
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderItemSerializer(BaseSerializerMixin):
    """Purchases order item serializer."""

    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for purchases order serialiser"""
        model = PurchaseOrderItem
        fields = '__all__'
