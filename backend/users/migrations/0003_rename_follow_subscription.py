# Generated by Django 4.1 on 2022-08-30 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follow',
            new_name='Subscription',
        ),
    ]
