# Generated by Django 2.2 on 2019-06-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0014_auto_20190620_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
