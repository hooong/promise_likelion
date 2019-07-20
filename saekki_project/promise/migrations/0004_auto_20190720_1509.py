# Generated by Django 2.2.2 on 2019-07-20 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promise', '0003_auto_20190709_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promise_comment',
            name='promise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='promise.Promise'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receive_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='firend_receive_user', to=settings.AUTH_USER_MODEL)),
                ('send_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='firend_send_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]