import logging

from django.db import migrations
from django.db.models import Q

from netbox_dns.models import ZoneStatusChoices


def delete_ptr_records_for_inactive_zones(apps, schema_editor):
    logger = logging.getLogger("django")

    Record = apps.get_model("netbox_dns", "Record")

    for record in Record.objects.exclude(
        Q(Q(ptr_record__isnull=True) | Q(zone__status=ZoneStatusChoices.STATUS_ACTIVE))
    ):
        logger.warning(
            "Deleting PTR for record %s:%s in zone %s",
            record.type,
            record.name,
            record.zone.name,
        )
        record.ptr_record.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_dns", "0014_add_view_description"),
        ("netbox_dns", "0015_add_record_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="record",
            options={"ordering": ("zone", "name", "type", "value", "status")},
        ),
        migrations.RunPython(delete_ptr_records_for_inactive_zones),
    ]
