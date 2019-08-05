# Generated by Django 2.2.2 on 2019-08-04 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promise', '0002_auto_20190804_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party_detail',
            name='fun_image',
        ),
        migrations.CreateModel(
            name='Fun_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fun_image', models.ImageField(blank=True, null=True, upload_to='promise_fun_tmp')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fun', to='promise.Party_detail')),
            ],
        ),
    ]