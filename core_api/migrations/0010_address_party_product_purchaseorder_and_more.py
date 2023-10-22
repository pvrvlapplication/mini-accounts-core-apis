# Generated by Django 4.2.4 on 2023-09-09 09:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core_api", "0009_remove_user_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dno", models.CharField(max_length=30)),
                ("area", models.CharField(max_length=30)),
                ("city", models.CharField(max_length=30)),
                ("district", models.CharField(max_length=25)),
                ("state", models.CharField(max_length=20)),
                ("country", models.CharField(max_length=20)),
                ("mobile", models.CharField(max_length=15)),
                (
                    "phone",
                    models.CharField(
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator(
                                "\\+?\\d[\\d -]{8,12}\\d",
                                message="Enter a Valid Indian Phone Number",
                            )
                        ],
                    ),
                ),
                ("primary", models.BooleanField(blank=True, null=True)),
                ("shipping", models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Party",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "gst",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "\\d{2}[A-Z]{5}\\d{4}[A-Z]{1}[A-Z\\d]{1}[Z]{1}[A-Z\\d]{1}",
                                message="Enter a Valid Indian GST Number",
                            )
                        ],
                    ),
                ),
                (
                    "pan",
                    models.CharField(
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator(
                                "[A-Z]{5}\\d{4}[A-Z]{1}",
                                message="Enter a Valid PAN Number",
                            )
                        ],
                    ),
                ),
                (
                    "party_type",
                    models.CharField(
                        choices=[("C", "CUSTOMER"), ("V", "VENDOR")], max_length=10
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "gst_slab",
                    models.CharField(
                        choices=[(0, 0), (5, 5), (12, 12), (18, 18), (28, 28)],
                        max_length=5,
                    ),
                ),
                ("hsn", models.CharField(max_length=35)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("po_number", models.CharField(max_length=50)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("comment", models.TextField()),
                (
                    "gst_type",
                    models.CharField(
                        choices=[("I", "INTER"), ("O", "OUTER"), ("NO", "NOGST")],
                        max_length=10,
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="po_address",
                        to="core_api.address",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_api.branch",
                    ),
                ),
                (
                    "shipping_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="po_shipping",
                        to="core_api.address",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core_api.party"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseOrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("sgst", models.DecimalField(decimal_places=2, max_digits=10)),
                ("cgst", models.DecimalField(decimal_places=2, max_digits=10)),
                ("igst", models.DecimalField(decimal_places=2, max_digits=10)),
                ("taxble_value", models.DecimalField(decimal_places=2, max_digits=15)),
                ("invoice_value", models.DecimalField(decimal_places=2, max_digits=20)),
                (
                    "po",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_api.purchaseorder",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_api.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="address",
            name="party",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core_api.party"
            ),
        ),
    ]