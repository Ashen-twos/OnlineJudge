# Generated by Django 3.2.9 on 2023-02-17 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0014_remove_submission_extra_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='raw_code',
            field=models.TextField(null=True),
        ),
    ]
