"""Debit side tasks."""
from kenmall_enterprise_portal.debit.models import Units
from kenmall_enterprise_portal.common.utils import get_edi_client

def compose_edi_units_payload(units, category):
    edi_units_payload = {
        'guid': units.id,
        "created_by":  units.created_by,
        "updated_by": units.updated_by,
        "enterprise": units.enterprise,
        "section": category.section.section_name,
        "category": category.category_name,
        "units_name": units.units_name,
        "units_code": units.units_code,
    }
    return edi_units_payload


def push_units_to_edi():
    client = get_edi_client()
    unpushed_units = Units.objects.filter(pushed_to_edi = False)

    for units in unpushed_units:
        categories = units.category.all()

        for category in categories:
            edi_units_payload = compose_edi_units_payload(units, category)
            units_response = client.units.create(edi_units_payload)
            if units_response.status_code == 201:
                units = Units.objects.get(id=edi_units_payload['guid'])
                units.pushed_to_edi = True
                units.save()
