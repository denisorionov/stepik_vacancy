# Generated by Django 3.0.8 on 2020-07-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vacancy', '0004_auto_20200719_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialty',
            name='picture',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
