# Generated by Django 3.0.8 on 2020-07-19 06:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vacancy', '0003_auto_20200719_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='test',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
