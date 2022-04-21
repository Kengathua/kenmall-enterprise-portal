from django.db import models
from django.utils import timezone

from kenmall_enterprise_portal.common.models import AbstractBase
from kenmall_enterprise_portal.debit.models import (
    Item
)
from kenmall_enterprise_portal.debit.tasks import push_units_to_edi
# Create your models here.
from kenmall_enterprise_portal.enterprises.models import Enterprise

TAX_TYPE_CHOICES = (
    ('FLAT', 'FLAT'),
    ('NO TAX', 'NO TAX'),
    ('PERCENTAGE', 'PERCENTAGE'),
)

PURCHASE_ORDER_STATUS = (
    ('PENDING', 'PENDING'),
    ('CANCELED', 'CANCELED'),
    ('FULFILLED', 'FULFILLED'),
)

FLAT = 'FLAT'
PENDING = 'PENDING'

class Purchase(AbstractBase):
    item = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.PROTECT)
    quantity_purchased = models.FloatField(null=False, blank=False)
    unit_price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=30, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now)
    marked_price = models.FloatField(null=True, blank=True)


class PurchaseOrder(AbstractBase):
    order_number = models.CharField(max_length=300, null=False, blank=False)
    requisition_no = models.CharField(max_length=300, null=True, blank=True)
    tracking_number = models.CharField(max_length=300, null=True, blank=True)
    vendor = models.ForeignKey(
        Enterprise, null=True, blank=True, on_delete=models.PROTECT)
    vendor_name = models.CharField(max_length=300,null=True, blank=True)
    sales_person = models.CharField(max_length=300, null=True, blank=True)
    contact_name = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    shipping_terms = models.CharField(max_length=300, null=True, blank=True)
    shipping_method = models.CharField(max_length=300, null=True, blank=True)
    order_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(null=True, blank=True)
    subtotal_amount = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=2)
    discount_amount = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=2)
    tax_type = models.CharField(max_length=300, choices=TAX_TYPE_CHOICES, default=FLAT)
    tax_percentage = models.FloatField(null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    excise_duty_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    other_costs = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    shipping_and_handling = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    net_total_amount = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=2)
    shipping_address = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=300, null=True, blank=True)
    carrier = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(
        max_length=300, choices=PURCHASE_ORDER_STATUS, default=PENDING)
    pushed_to_edi = models.BooleanField(default=False)

    @property
    def order_summary(self):
        purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order=self)
        discounts = []
        amounts = []
        if purchase_order_items.exists():
            for purchase_order_item in purchase_order_items:
                discounts.append(purchase_order_item.discount_amount)
                amounts.append(purchase_order_item.amount)

        total_discount = sum(discounts)
        subtotal = sum(amounts)
        net_total_amount = subtotal - total_discount - self.tax_amount \
            - self.excise_duty_amount - self.shipping_and_handling - self.other_costs

        summary = {
            'subtotal_amount': subtotal,
            'discount_amount': total_discount,
            'tax_amount': self.tax_amount,
            'excise_duty': self.excise_duty_amount,
            'shipping_and_handling': self.shipping_and_handling,
            'other_costs': self.other_costs,
            'net_total': net_total_amount,
        }

        return summary


    def validate_vendor_details_added(self):
        if not self.vendor and not self.vendor_name:
            import pdb
            pdb.set_trace()

    def clean(self) -> None:
        self.validate_vendor_details_added()
        return super().clean()

    def get_vendor_details(self):
        from kenmall_enterprise_portal.enterprises.models import Enterprise, EnterpriseContacts
        if self.vendor:
            self.vendor_name = self.vendor.name
            enterprise_contacts = EnterpriseContacts.objects.filter(enterprise=self.vendor)
            if enterprise_contacts.exists():
                enterprise_contact = enterprise_contacts.first()
                self.phone_number = enterprise_contact.phone_number
                self.email = enterprise_contact.email
                self.shipping_address = enterprise_contact.address

    def save(self, *args, **kwargs):
        self.get_vendor_details()
        super().save(*args, **kwargs)


class PurchaseOrderItem(AbstractBase):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.PROTECT)
    code = models.CharField(max_length=300)
    product = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.PROTECT)
    product_description = models.CharField(
        null=True, blank=True, max_length=300)
    quantity_to_order = models.FloatField()
    unit_price = models.DecimalField(max_digits=30, decimal_places=2)
    unit_discount = models.DecimalField(
        max_digits=30, decimal_places=2, default=0)
    discount_amount = models.DecimalField(
        max_digits=30, decimal_places=2, default=0)
    amount = models.DecimalField(
        null=True, blank=True, max_digits=30, decimal_places=2)
    status = models.CharField(
        max_length=300, choices=PURCHASE_ORDER_STATUS, default=PENDING)
    pushed_to_edi = models.BooleanField(default=False)

    def get_product_details(self):
        if self.product:
            self.product_description = f'{self.product.make_year}  {self.product.item_name}'

    def get_amount(self):
        amount = float(self.unit_price) * self.quantity_to_order
        self.amount = amount

    def save(self, *args, **kwargs):
        self.get_amount()
        self.get_product_details()
        super().save(*args, **kwargs)
