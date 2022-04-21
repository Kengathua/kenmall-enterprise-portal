"""Catalog url."""
from rest_framework import routers
from django.urls import path, include
from kenmall_enterprise_portal.catalog import views

router = routers.DefaultRouter()
router.register(r'catalog', views.CatalogViewSet)

urlpatterns = [
    path('catalog/', include(router.urls)),
]
