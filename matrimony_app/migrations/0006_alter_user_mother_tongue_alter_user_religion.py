# Generated by Django 4.2 on 2023-05-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony_app', '0005_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mother_tongue',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='religion',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
