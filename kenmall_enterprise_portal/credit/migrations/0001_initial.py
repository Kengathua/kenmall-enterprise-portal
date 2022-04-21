# Generated by Django 3.2.12 on 2022-06-22 16:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprises', '0003_rename_bus_reg_no_enterprise_business_registration_number'),
        ('debit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('created_by', models.UUIDField(editable=False)),
                ('updated_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField()),
                ('enterprise', models.CharField(max_length=250)),
                ('order_number', models.CharField(max_length=300)),
                ('requisition_no', models.CharField(blank=True, max_length=300, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=300, null=True)),
                ('vendor_name', models.CharField(blank=True, max_length=300, null=True)),
                ('sales_person', models.CharField(blank=True, max_length=300, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=300, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('shipping_terms', models.CharField(blank=True, max_length=300, null=True)),
                ('shipping_method', models.CharField(blank=True, max_length=300, null=True)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('due_date', models.DateField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('subtotal_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('tax_type', models.CharField(choices=[('FLAT', 'FLAT'), ('NO TAX', 'NO TAX'), ('PERCENTAGE', 'PERCENTAGE')], default='FLAT', max_length=300)),
                ('tax_percentage', models.FloatField(blank=True, null=True)),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('excise_duty_amount', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('other_costs', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('shipping_and_handling', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('net_total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('shipping_address', models.TextField(blank=True, null=True)),
                ('billing_address', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('subject', models.CharField(blank=True, max_length=300, null=True)),
                ('carrier', models.CharField(blank=True, max_length=300, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('CANCELED', 'CANCELED'), ('FULFILLED', 'FULFILLED')], default='PENDING', max_length=300)),
                ('pushed_to_edi', models.BooleanField(default=False)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='enterprises.enterprise')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('created_by', models.UUIDField(editable=False)),
                ('updated_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField()),
                ('enterprise', models.CharField(max_length=250)),
                ('code', models.CharField(max_length=300)),
                ('product_description', models.CharField(blank=True, max_length=300, null=True)),
                ('quantity_to_order', models.FloatField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=30)),
                ('unit_discount', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('CANCELED', 'CANCELED'), ('FULFILLED', 'FULFILLED')], default='PENDING', max_length=300)),
                ('pushed_to_edi', models.BooleanField(default=False)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='debit.item')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='credit.purchaseorder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('created_by', models.UUIDField(editable=False)),
                ('updated_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField()),
                ('enterprise', models.CharField(max_length=250)),
                ('quantity_purchased', models.FloatField()),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=30)),
                ('purchase_date', models.DateField(default=django.utils.timezone.now)),
                ('marked_price', models.FloatField(blank=True, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='debit.item')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
