# Generated by Django 4.2.4 on 2023-09-13 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0012_purchaseorder_invoice_value_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('invoice_no', models.CharField(max_length=35)),
                ('po', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.purchaseorder')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('invoice_no', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='SaleOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_number', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('gst_type', models.CharField(choices=[('I', 'INTER'), ('O', 'OUTER'), ('NO', 'NOGST')], max_length=10)),
                ('taxble_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('invoice_value', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='so_address', to='core_api.address')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.branch')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='so_shipping', to='core_api.address')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.party')),
            ],
        ),
        migrations.CreateModel(
            name='SaleOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('taxble_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('invoice_value', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.product')),
                ('so', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.saleorder')),
            ],
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('taxble_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('invoice_value', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.sale')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='so',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.saleorder'),
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('taxble_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('invoice_value', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.purchase')),
            ],
        ),
    ]
