# Generated by Django 4.2 on 2023-04-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony_app', '0002_alter_user_age_alter_user_gender_alter_user_religion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mother_tongue',
            field=models.CharField(default='', max_length=255),
        ),
    ]
