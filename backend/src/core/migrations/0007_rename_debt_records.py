# Generated by Django 4.2.11 on 2024-05-04 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_debt_clear'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Debt',
            new_name='Records',
        ),
    ]