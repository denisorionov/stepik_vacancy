# Generated by Django 3.0.8 on 2020-07-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vacancy', '0006_auto_20200726_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default=None, height_field='height_field', null=True, upload_to='company_images',
                                    width_field='width_field'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(default=None, height_field='height_field', null=True, upload_to='speciality_images',
                                    width_field='width_field'),
        ),
    ]
