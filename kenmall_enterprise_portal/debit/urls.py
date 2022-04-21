"""Urls file for debit app."""
from rest_framework import routers
from django.urls import path, include

from kenmall_enterprise_portal.debit import views

router = routers.DefaultRouter()
router.register(r'sections', views.SectionViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'item_types', views.ItemTypeViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'item_models', views.ItemModelViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'units', views.UnitsViewSet)
router.register(r'inventories', views.InventoryViewSet)

urlpatterns = [
    path('debit/', include(router.urls)),
]
