# Generated by Django 3.0.8 on 2020-07-19 06:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vacancy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
