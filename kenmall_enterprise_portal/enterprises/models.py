from django.db import models
from django.db.models import PROTECT

from kenmall_enterprise_portal.common.models import AbstractBaseClass
from kenmall_enterprise_portal.common.validators import phoneNumberRegex


ENTERPRISE_TYPES = (
    ('RETAILER', 'RETAILER'),
    ('SUPPLIER','SUPPLIER'),
)
class EnterpriseBase(AbstractBaseClass):
    pass

    class Meta:
        """Meta class for enterprise base class"""

        abstract = True


class Enterprise(EnterpriseBase):
    business_registration_number = models.CharField(max_length=300, null=False, blank= False)
    name = models.CharField(max_length=300, null=False, blank=False)
    kenmall_code = models.CharField(max_length=300,  null=False, blank=False)
    partnership_type = models.CharField(max_length=300, null=False, blank=False, choices=ENTERPRISE_TYPES)
    dissolution_date = models.DateField(db_index=True, null=True, blank=True)
    dissolution_reason = models.TextField(null=True, blank= True)


class EnterpriseContacts(EnterpriseBase):
    enterprise = models.ForeignKey(Enterprise, max_length=250, null=False,
                                  blank=False, related_name='contact_franchise_name', on_delete=PROTECT)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16, unique=True, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
