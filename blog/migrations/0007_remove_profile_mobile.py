# Generated by Django 5.0.3 on 2024-09-19 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_profile_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
    ]
