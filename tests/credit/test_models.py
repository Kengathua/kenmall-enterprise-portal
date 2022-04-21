from django.test import TestCase
from kenmall_enterprise_portal.debit.models import (
    Section, Category, Brand, ItemModel, Units, Item)
from kenmall_enterprise_portal.credit.models import (
    Purchase, PurchaseOrder, PurchaseOrderItem
)
from kenmall_enterprise_portal.enterprises.models import (
    Enterprise, EnterpriseContacts)

from model_bakery import baker


class TestPurchase(TestCase):

    def test_create_purchase(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        purchase = baker.make(Purchase, item=item, quantity_purchased=10, total_price=3000, )

        assert purchase
        assert Purchase.objects.count() == 1


class TestPurchaseOrder(TestCase):

    def test_create_purchase_order(self):
        vendor = baker.make(
            Enterprise, name='Test Vendor', kenmall_code=3030, partnership_type='SUPPLIER')
        baker.make(
            EnterpriseContacts, enterprise=vendor, phone_number='0787653890',
            email='testvendor@email.com', address='PO BOX 455-01000')
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        purchase_order = baker.make(
            PurchaseOrder, vendor=vendor, shipping_terms='Freight on Board',
            discount_amount=200, shipping_method='Air & Land')

        assert purchase_order
        assert PurchaseOrder.objects.count() == 1


class TestPurchaseItemOrder(TestCase):

    def test_create_purchase_order_item(self):
        vendor = baker.make(
            Enterprise, name='Test Vendor', kenmall_code=3030, partnership_type='SUPPLIER')
        baker.make(
            EnterpriseContacts, enterprise=vendor, phone_number='0787653890',
            email='testvendor@email.com', address='PO BOX 455-01000')
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        purchase_order = baker.make(
            PurchaseOrder, vendor=vendor, shipping_terms='Freight on Board',
            discount_amount=200, shipping_method='Air & Land')
        purchase_order_item = baker.make(
            PurchaseOrderItem, purchase_order=purchase_order, product=item,
            quantity_to_order=10, amount=2000, code='#234590', unit_price=200)

        assert purchase_order_item
        assert PurchaseOrderItem.objects.count() == 1
