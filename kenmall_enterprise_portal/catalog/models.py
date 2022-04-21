from django.db import models

from kenmall_enterprise_portal.common.models import AbstractBase
from kenmall_enterprise_portal.debit.models import Inventory

CURRENCY_CHOICES = (
    ('KSH', 'KSH'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('CAD', 'CAD'),
    ('AUD', 'AUD'),
)

KSH = 'KSH'

class Catalog(AbstractBase):
    inventory_item = models.OneToOneField(
        Inventory, null=False, blank=False, unique=True, on_delete=models.PROTECT)
    marked_price = models.FloatField(null=True, blank=True)
    discount_amount = models.FloatField(null=False, blank=False, default=0)
    selling_price = models.FloatField(null=True, blank=True)
    currency = models.CharField(
        null=False, blank=False, max_length=250, choices=CURRENCY_CHOICES, default=KSH)
    quantity = models.FloatField(default=0)
    on_display = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    pushed_to_edi = models.BooleanField(default=False)
