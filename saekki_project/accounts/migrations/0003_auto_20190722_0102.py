# Generated by Django 2.2.2 on 2019-07-22 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190722_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]