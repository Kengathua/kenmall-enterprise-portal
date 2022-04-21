"""Credit side urls."""

from rest_framework import routers
from django.urls import path, include

from kenmall_enterprise_portal.credit import views

router = routers.DefaultRouter()

router.register(r'purchases_order', views.PurchaseOrderViewSet)
router.register(r'purchases_order_item', views.PurchaseOrderItemViewSet)

urlpatterns = [
    path('credit/', include(router.urls)),
]