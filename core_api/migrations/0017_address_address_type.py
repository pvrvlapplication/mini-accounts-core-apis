# Generated by Django 4.2.4 on 2023-11-25 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_api", "0016_remove_purchaseorderitem_po_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="address_type",
            field=models.CharField(
                choices=[
                    ("HM", "HOME"),
                    ("BU", "BUSINESS"),
                    ("BI", "BILLING"),
                    ("SH", "SHIPPING"),
                ],
                default=1,
                max_length=3,
            ),
            preserve_default=False,
        ),
    ]
