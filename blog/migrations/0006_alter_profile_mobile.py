# Generated by Django 5.0.3 on 2024-09-19 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_profile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=15),
        ),
    ]
