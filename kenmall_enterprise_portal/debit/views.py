from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet


from kenmall_enterprise_portal.debit.models import (
    Category, Section, ItemType, Brand, ItemModel,
    Item, Units, Inventory)
from kenmall_enterprise_portal.debit import serializers


class SectionViewSet(ModelViewSet):
    """Viewset for the Section model."""
    queryset = Section.objects.all()
    serializer_class = serializers.SectionSerializer


class CategoryViewSet(ModelViewSet):
    """Viewset for the Category model"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ItemTypeViewSet(ModelViewSet):
    """Viewset for the ItemType model"""
    queryset = ItemType.objects.all()
    serializer_class = serializers.ItemTypeSerializer


class BrandViewSet(ModelViewSet):
    """Viewset for the Brand model"""
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializer


class ItemModelViewSet(ModelViewSet):
    """Viewset for the ItemModel model"""
    queryset = ItemModel.objects.all()
    serializer_class = serializers.ItemModelSerializer


class ItemViewSet(ModelViewSet):
    """Viewset for the Item model"""
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer


class UnitsViewSet(ModelViewSet):
    """Viewset for the Units model"""
    queryset = Units.objects.all()
    serializer_class = serializers.UnitsSerializer


class InventoryViewSet(ModelViewSet):
    """Viewset for the Inventory model"""
    queryset = Inventory.objects.all()
    serializer_class = serializers.InventorySerializer
