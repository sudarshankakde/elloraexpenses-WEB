# Generated by Django 4.2.7 on 2024-02-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ENSApp", "0016_alter_daily_attendance_date_alter_punch_in_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="daily_attendance",
            name="date",
            field=models.DateField(default="2024-02-02"),
        ),
        migrations.AlterField(
            model_name="punch_in",
            name="date",
            field=models.DateField(default="2024-02-02"),
        ),
        migrations.AlterField(
            model_name="punch_out",
            name="date",
            field=models.DateField(default="2024-02-02"),
        ),
        migrations.AlterField(
            model_name="total_expense",
            name="date",
            field=models.DateField(default="2024-02-02"),
        ),
    ]