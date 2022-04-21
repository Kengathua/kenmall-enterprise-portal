from kenmall_enterprise_portal.common.serializers import BaseSerializerMixin
from kenmall_enterprise_portal.catalog import models

class CatalogSerializer(BaseSerializerMixin):
    """Catalog model serializer class."""

    class Meta:
        """Meta class for catalog serializer."""
        model = models.Catalog
        fields = "__all__"
