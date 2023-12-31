# Generated by Django 4.2.4 on 2023-11-11 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0015_alter_purchaseorder_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorderitem',
            name='po',
        ),
        migrations.RemoveField(
            model_name='purchaseorderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='po',
        ),
        migrations.AddField(
            model_name='purchase',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='po_address', to='core_api.address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='comment',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='gst_type',
            field=models.CharField(choices=[('I', 'INTER'), ('O', 'OUTER'), ('NO', 'NOGST')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='shipping_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='po_shipping', to='core_api.address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core_api.party'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PurchaseOrder',
        ),
        migrations.DeleteModel(
            name='PurchaseOrderItem',
        ),
    ]
