# Generated by Django 3.0.8 on 2020-08-03 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vacancy', '0011_auto_20200803_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default=None, height_field='height_field', null=True, upload_to='logo',
                                    width_field='width_field'),
        ),
    ]
