# Generated by Django 4.2.11 on 2024-05-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_debt_pokerid2_debt_wol_debt_clear_debt_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='debt',
            name='Balance',
            field=models.FloatField(default=0.0),
        ),
    ]