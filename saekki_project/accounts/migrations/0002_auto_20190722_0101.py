# Generated by Django 2.2.2 on 2019-07-22 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profie',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]