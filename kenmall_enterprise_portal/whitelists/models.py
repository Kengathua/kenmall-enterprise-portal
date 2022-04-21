import imp
from django.db import models

# Create your models here.
from kenmall_enterprise_portal.common.models import AbstractBase

class Whitelist(AbstractBase):
    product_code = models.CharField(null=True, blank=True, max_length=300)
    is_available = models.BooleanField(default=True)