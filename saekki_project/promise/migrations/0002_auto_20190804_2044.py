# Generated by Django 2.2.2 on 2019-08-04 20:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promise', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promise',
            old_name='party',
            new_name='pre_party',
        ),
        migrations.AddField(
            model_name='party_detail',
            name='acpt',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='party_detail',
            name='fun_image',
            field=models.ImageField(blank=True, null=True, upload_to='promise_fun_tmp'),
        ),
        migrations.AddField(
            model_name='promise',
            name='acpt_party',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), blank=True, default=list, null=True, size=None),
        ),
    ]
