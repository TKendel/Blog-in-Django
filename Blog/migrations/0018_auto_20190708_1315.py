# Generated by Django 2.2 on 2019-07-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0017_auto_20190706_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='contact_address',
            field=models.CharField(default='test', max_length=255),
        ),
        migrations.AlterField(
            model_name='settings',
            name='contact_number',
            field=models.CharField(default='000', max_length=255),
        ),
        migrations.AlterField(
            model_name='settings',
            name='email',
            field=models.EmailField(default='test@test.com', max_length=255),
        ),
        migrations.AlterField(
            model_name='settings',
            name='siteName',
            field=models.CharField(default='test', max_length=255),
        ),
    ]
