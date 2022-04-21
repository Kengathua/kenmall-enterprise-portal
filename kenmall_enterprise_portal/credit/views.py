from django.shortcuts import render
from rest_framework import viewsets

from kenmall_enterprise_portal.credit.models import PurchaseOrder, PurchaseOrderItem
from kenmall_enterprise_portal.credit import serializers


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """Purchases Order Viewset."""

    queryset = PurchaseOrder.objects.all().order_by('-updated_on')
    serializer_class = serializers.PurchaseOrderSerializer


class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    """Purchases Order Viewset."""

    queryset = PurchaseOrderItem.objects.all().order_by('-updated_on')
    serializer_class = serializers.PurchaseOrderItemSerializer
