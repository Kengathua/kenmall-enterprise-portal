# Generated by Django 3.2.12 on 2022-06-21 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0002_auto_20220615_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enterprise',
            old_name='bus_reg_no',
            new_name='business_registration_number',
        ),
    ]