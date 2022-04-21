"""EDI Debit side model serializers file."""
from rest_framework import serializers

from kenmall_enterprise_portal.debit.models import (
    Section, Category, Units, Item, Inventory)
from kenmall_enterprise_portal.common.serializers import BaseSerializerMixin
from kenmall_enterprise_portal.debit import models

class SectionSerializer(BaseSerializerMixin):
    """Serializer class for the Section model."""
    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for SectionSerializer."""

        model = Section
        fields = '__all__'


class CategorySerializer(BaseSerializerMixin):
    """Serializer class for the Category model."""
    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for CategorySerializer."""

        model = Category
        fields = '__all__'


class ItemTypeSerializer(BaseSerializerMixin):
    """Serializer class for the ItemType model."""
    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for ItemTypeSerializer."""

        model = models.ItemType
        fields = '__all__'


class BrandSerializer(BaseSerializerMixin):
    """Serializer class for the Brand model."""
    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for BrandSerializer."""

        model = models.Brand
        fields = '__all__'


class ItemModelSerializer(BaseSerializerMixin):
    """Serializer class for the Model model."""
    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for ModelSerializer."""

        model = models.ItemModel
        fields = '__all__'


class ItemSerializer(BaseSerializerMixin):
    """Serializer class for the Units model."""
    created_by = serializers.UUIDField()
    # category = CategorySerializer(read_only=True, many=True)

    class Meta:
        """Meta class for UnitsSerializer."""

        model = models.Item
        fields = '__all__'


class UnitsSerializer(BaseSerializerMixin):
    """Serializer class for the Units model."""
    created_by = serializers.UUIDField()
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        """Meta class for UnitsSerializer."""

        model = models.Units
        fields = '__all__'


class InventorySerializer(BaseSerializerMixin):
    """Serializer class for the Inventory model."""
    created_by = serializers.UUIDField()

    class Meta:
        """Meta class for InventorySerializer."""

        model = models.Inventory
        fields = '__all__'
