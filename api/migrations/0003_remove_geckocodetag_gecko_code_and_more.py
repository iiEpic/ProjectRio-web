# Generated by Django 5.0.7 on 2024-07-29 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_comm_type_community_community_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geckocodetag',
            name='gecko_code',
        ),
        migrations.RemoveField(
            model_name='geckocodetag',
            name='gecko_code_desc',
        ),
        migrations.AddField(
            model_name='geckocodetag',
            name='code',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='geckocodetag',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
