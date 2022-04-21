"""Catalog views file."""
from rest_framework import viewsets
from kenmall_enterprise_portal.catalog.models import (
    Catalog)
from kenmall_enterprise_portal.catalog import serializers

class CatalogViewSet(viewsets.ModelViewSet):
    """Catalog viewset class."""

    queryset = Catalog.objects.all().order_by('-updated_on')
    serializer_class = serializers.CatalogSerializer
