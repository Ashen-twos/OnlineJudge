# Generated by Django 3.2.9 on 2023-02-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0019_auto_20230221_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='judge_config',
            field=models.JSONField(default=dict),
        ),
    ]
