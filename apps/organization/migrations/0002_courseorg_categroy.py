# Generated by Django 2.0.2 on 2018-03-27 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='categroy',
            field=models.TextField(choices=[('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高效')], default='gr', max_length=10, verbose_name='机构类别'),
        ),
    ]
