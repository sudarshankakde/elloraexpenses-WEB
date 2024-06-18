# Generated by Django 4.2.7 on 2024-06-18 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ENSApp', '0019_punch_out_other_expenses_punch_out_toll_parkking'),
    ]

    operations = [
        migrations.AddField(
            model_name='total_expense',
            name='other_expenses',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='other_expenses'),
        ),
        migrations.AddField(
            model_name='total_expense',
            name='toll_parkking',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Toll/Fastag/Parking'),
        ),
    ]
