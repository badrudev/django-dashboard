# Generated by Django 5.1.1 on 2024-10-26 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_customer_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='username',
        ),
    ]
