# Generated by Django 2.2.2 on 2019-08-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification_penalty',
            name='final',
            field=models.CharField(default='0', max_length=5),
        ),
    ]