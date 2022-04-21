import pytest
from kenmall_enterprise_portal.credit.tasks import push_purchases_orders_to_edi
from kenmall_enterprise_portal.debit.models import (
    Section, Category, Brand, ItemModel, Units, Item)
from kenmall_enterprise_portal.credit.models import (
    Purchase, PurchaseOrder, PurchaseOrderItem
)
from kenmall_enterprise_portal.enterprises.models import (
    Enterprise, EnterpriseContacts)

from model_bakery import baker

pytestmark = pytest.mark.django_db
def test_push_purchases_orders_to_edi():
    enterprise = baker.make(
        Enterprise, name='Test Enterprise', kenmall_code=2020,
        business_registration_number='PVLC87654', partnership_type='RETAILER')
    enterprise_code = enterprise.kenmall_code
    baker.make(
        EnterpriseContacts, enterprise=enterprise, phone_number='+254785858545',
        email='testent@enterprise.com', address='PO BOX 2345-02000')
    vendor = baker.make(
        Enterprise, name='Test Vendor', kenmall_code=3030, partnership_type='SUPPLIER')
    baker.make(
        EnterpriseContacts, enterprise=vendor, phone_number='+25478765389',
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
        PurchaseOrder, order_number='#98763', tracking_number='#76548', requisition_no='#876584', vendor=vendor,
        shipping_terms='Freight on Board', discount_amount=200, shipping_method='Air & Land',
        enterprise=enterprise_code)
    purchase_order_item = baker.make(
            PurchaseOrderItem, purchase_order=purchase_order, product=item,
            quantity_to_order=10, amount=2000, code='#234590', unit_price=200, enterprise=enterprise_code)
    purchase_order_item = baker.make(
            PurchaseOrderItem, purchase_order=purchase_order, product=item,
            quantity_to_order=10, amount=2000, code='#234590', unit_price=200, enterprise=enterprise_code)

    assert purchase_order
    assert purchase_order_item
    assert purchase_order.pushed_to_edi == False
    push_purchases_orders_to_edi()
    purchase_order.refresh_from_db()
    assert purchase_order.pushed_to_edi == True


pytestmark = pytest.mark.django_db
def test_push_purchases_orders_items_to_edi():
    enterprise = baker.make(
        Enterprise, name='Test Enterprise', kenmall_code=2020,
        business_registration_number='PVLC87654', partnership_type='RETAILER')
    enterprise_code = enterprise.kenmall_code
    baker.make(
        EnterpriseContacts, enterprise=enterprise, phone_number='+254785858545',
        email='testent@enterprise.com', address='PO BOX 2345-02000')
    vendor = baker.make(
        Enterprise, name='Test Vendor', kenmall_code=3030, partnership_type='SUPPLIER')
    baker.make(
        EnterpriseContacts, enterprise=vendor, phone_number='+25478765389',
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
        PurchaseOrder, order_number='#98763', tracking_number='#76548',
        requisition_no='#876584', vendor=vendor, shipping_terms='Freight on Board',
        discount_amount=200, shipping_method='Air & Land', pushed_to_edi=True,
        enterprise=enterprise_code)
    purchase_order_item1 = baker.make(
            PurchaseOrderItem, purchase_order=purchase_order, product=item,
            quantity_to_order=10, amount=2000, code='#234590', unit_price=200, enterprise=enterprise_code)
    purchase_order_item2 = baker.make(
            PurchaseOrderItem, purchase_order=purchase_order, product=item,
            quantity_to_order=10, amount=2000, code='#234590', unit_price=200, enterprise=enterprise_code)

    assert purchase_order
    assert purchase_order_item1
    assert purchase_order_item2
    assert purchase_order_item1.pushed_to_edi == False
    assert purchase_order_item2.pushed_to_edi == False

    push_purchases_orders_to_edi()
    purchase_order_item1.refresh_from_db()
    purchase_order_item2.refresh_from_db()

    assert purchase_order_item1.pushed_to_edi == True
    assert purchase_order_item2.pushed_to_edi == True
