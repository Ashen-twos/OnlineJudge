# Generated by Django 3.2.9 on 2023-02-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0015_auto_20230210_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='extra_score',
            field=models.JSONField(default=dict),
        ),
    ]
