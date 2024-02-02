# Generated by Django 4.2.7 on 2024-02-02 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ENSApp", "0014_alter_punch_in_date_alter_punch_out_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="punch_in",
            name="manual_reading",
            field=models.IntegerField(
                blank=True, default=0, null=True, verbose_name="Manual Reading"
            ),
        ),
        migrations.AlterField(
            model_name="punch_in",
            name="meter_photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="meter_photos/",
                verbose_name="Meter Photo",
            ),
        ),
        migrations.AlterField(
            model_name="punch_in",
            name="ticket_amount",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="punch_in",
            name="ticket_photo",
            field=models.ImageField(blank=True, null=True, upload_to="meter_photos/"),
        ),
        migrations.AlterField(
            model_name="punch_out",
            name="daily_allounce",
            field=models.IntegerField(
                blank=True, default=0, null=True, verbose_name="DA"
            ),
        ),
        migrations.AlterField(
            model_name="punch_out",
            name="lodging",
            field=models.IntegerField(
                blank=True, default=0, null=True, verbose_name="Lodging/Boarding"
            ),
        ),
        migrations.AlterField(
            model_name="punch_out",
            name="meter_photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="meter_photos/",
                verbose_name="Meter Photo",
            ),
        ),
        migrations.AlterField(
            model_name="punch_out",
            name="ticket_amount",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="punch_out",
            name="ticket_photo",
            field=models.ImageField(blank=True, null=True, upload_to="meter_photos/"),
        ),
    ]