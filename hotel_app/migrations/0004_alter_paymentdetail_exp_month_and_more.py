# Generated by Django 5.1.2 on 2024-11-11 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0003_alter_paymentdetail_exp_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetail',
            name='exp_month',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='exp_year',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
