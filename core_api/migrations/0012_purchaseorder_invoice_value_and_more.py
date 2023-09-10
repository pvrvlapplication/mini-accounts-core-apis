# Generated by Django 4.2.4 on 2023-09-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_api", "0011_alter_address_phone_alter_purchaseorderitem_cgst_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchaseorder",
            name="invoice_value",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=20, null=True
            ),
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="taxble_value",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=15, null=True
            ),
        ),
    ]
