# Generated by Django 4.2.5 on 2023-11-17 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practiceapp', '0006_rename_user_users_alter_orders_total'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order_pet',
            new_name='Order_product',
        ),
    ]
