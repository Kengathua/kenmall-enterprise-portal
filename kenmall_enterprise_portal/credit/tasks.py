from datetime import datetime
from xml.dom import ValidationErr
from django.utils import timezone
from kenmall_enterprise_portal.credit.models import (
    PurchaseOrder, PurchaseOrderItem)
from kenmall_enterprise_portal.enterprises.models import *
from django.core.exceptions import ValidationError

# from kenmall_enterprise_portal.edi_client.client import EDI
from kenmall_enterprise_portal.common.utils import get_edi_client

def process_edi_date(date):
    """Process edi date."""

    return timezone.make_aware(datetime.combine(date, datetime.min.time()))

def serialize_purchase_order_items(purchase_order):
    products_order_items = PurchaseOrderItem.objects.filter(
    purchase_order=purchase_order, pushed_to_edi=False)
    order_products = []
    if products_order_items.exists():
        for products_order_item in products_order_items:
            details = {
                'created_by': products_order_item.created_by,
                'updated_by': products_order_item.updated_by,
                'enterprise': products_order_item.enterprise,
                'guid': products_order_item.id,
                'purchase_order_guid': purchase_order.id,
                'code': products_order_item.code,
                'product_description': products_order_item.product_description,
                'quantity': float(products_order_item.quantity_to_order),
                'unit_price': float(products_order_item.unit_price),
                'unit_discount': float(products_order_item.unit_discount),
                'discount_amount': float(products_order_item.discount_amount),
                'amount': products_order_item.amount,
            }

            order_products.append(details)

    return order_products


def serialize_purchase_order(purchase_order):
    order_products = serialize_purchase_order_items(purchase_order)
    enterprise = Enterprise.objects.get(kenmall_code=purchase_order.enterprise)
    enterprise_contacts = EnterpriseContacts.objects.filter(enterprise=enterprise)

    if enterprise_contacts.exists() and not purchase_order.shipping_address:
        enterprise_contact =enterprise_contacts.first()
        shipping_address = f'{enterprise_contact.address}, {enterprise_contact.phone_number}, {enterprise_contact.email}'

    else:
        shipping_address = purchase_order.shipping_address

    if purchase_order.vendor and not purchase_order.billing_address:
        vendor_contact = EnterpriseContacts.objects.get(enterprise=purchase_order.vendor)
        billing_address = f'{vendor_contact.address}, {vendor_contact.phone_number}, {vendor_contact.email}'

    else:
        billing_address = purchase_order.billing_address

    purchase_order_payload = {
        'customer_kenmall_code':purchase_order.enterprise,
        'customer_name': enterprise.name,
        'order_number': purchase_order.order_number,
        'subject': purchase_order.subject,
        'requisition_no': purchase_order.requisition_no if purchase_order.requisition_no else None,
        'tracking_number': purchase_order.tracking_number if purchase_order.tracking_number else None,
        'contact_name': purchase_order.contact_name if purchase_order.contact_name else None,
        'carrier': purchase_order.carrier if purchase_order.carrier else None,
        'order_date': process_edi_date(purchase_order.order_date),
        'due_date': process_edi_date(purchase_order.due_date) if purchase_order.due_date else None,
        'excise_duty': purchase_order.order_summary['excise_duty'],
        'shipping_address': shipping_address,
        'billing_address': billing_address,
        'guid': purchase_order.id,
        'created_by': purchase_order.created_by,
        'updated_by': purchase_order.updated_by,
        'enterprise': purchase_order.enterprise,
        'vendor_kenmall_code': purchase_order.vendor.kenmall_code,
        'vendor_name': purchase_order.vendor_name,
        'sales_person': purchase_order.sales_person,
        'phone_number': purchase_order.phone_number,
        'email': purchase_order.email,
        'shipping_terms': purchase_order.shipping_terms,
        'shipping_method': purchase_order.shipping_method,
        'delivery_date': process_edi_date(purchase_order.delivery_date) if purchase_order.delivery_date else None,
        'subtotal_amount': purchase_order.order_summary['subtotal_amount'],
        'discount_amount': purchase_order.order_summary['discount_amount'],
        'tax_amount': purchase_order.order_summary['tax_amount'],
        'other_costs': purchase_order.order_summary['other_costs'],
        'shipping_and_handling': purchase_order.order_summary['shipping_and_handling'],
        'net_total_amount': purchase_order.order_summary['net_total'],
        'note': purchase_order.note,
    }

    return purchase_order_payload, order_products


def push_purchases_orders_to_edi():
    unpushed_purchase_orders = PurchaseOrder.objects.filter(pushed_to_edi=False)
    unpushed_purchase_order_items  = PurchaseOrderItem.objects.filter(pushed_to_edi=False)
    client = get_edi_client()

    for purchase_order in unpushed_purchase_orders:
        purchase_order_payload, edi_purchase_order_items_payloads = serialize_purchase_order(purchase_order)
        order_response = client.purchases_orders.create(purchase_order_payload)
        if order_response.status_code == 201:
            purchase_order.pushed_to_edi = True
            purchase_order.save()

        if edi_purchase_order_items_payloads:
            for edi_purchase_order_items_payload in edi_purchase_order_items_payloads:
                item_response = client.purshases_order_items.create(edi_purchase_order_items_payload)
                if item_response.status_code == 201:
                    order_item = PurchaseOrderItem.objects.get(id=edi_purchase_order_items_payload['guid'])
                    order_item.pushed_to_edi = True
                    order_item.save()

    if unpushed_purchase_order_items and not unpushed_purchase_orders:
        for unpushed_purchases_item in unpushed_purchase_order_items:
            purchase_order = unpushed_purchases_item.purchase_order
            edi_purchase_order_items_payloads = serialize_purchase_order_items(purchase_order)
            for edi_purchase_order_items_payload in edi_purchase_order_items_payloads:
                item_response = client.purshases_order_items.create(edi_purchase_order_items_payload)
                if item_response.status_code == 201:
                    order_item = PurchaseOrderItem.objects.get(id=edi_purchase_order_items_payload['guid'])
                    order_item.pushed_to_edi = True
                    order_item.save()
