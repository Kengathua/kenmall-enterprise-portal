# Generated by Django 3.2.12 on 2022-04-03 21:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('created_by', models.UUIDField(editable=False)),
                ('updated_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField()),
                ('bus_reg_no', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=300)),
                ('kenmall_code', models.CharField(max_length=300)),
                ('partnership_type', models.CharField(choices=[('RETAILER', 'RETAILER'), ('SUPPLIER', 'SUPPLIER')], max_length=300)),
                ('dissolution_date', models.DateField(blank=True, db_index=True, null=True)),
                ('dissolution_reason', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnterpriseContacts',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('created_by', models.UUIDField(editable=False)),
                ('updated_on', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phoneNumber', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('address', models.TextField(blank=True, null=True)),
                ('franchise', models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.PROTECT, related_name='contact_franchise_name', to='enterprises.enterprise')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]