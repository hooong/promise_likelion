# Generated by Django 2.2.2 on 2019-08-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190802_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state_msg',
            field=models.CharField(default='상태메시지를 입력해주세요.', max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
