# Generated by Django 4.2.11 on 2024-05-01 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_debttransaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DebtTransaction',
        ),
    ]
