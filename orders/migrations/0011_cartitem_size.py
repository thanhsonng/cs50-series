# Generated by Django 2.2.4 on 2019-08-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_cartitem_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
