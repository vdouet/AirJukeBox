# Generated by Django 3.2.5 on 2021-07-09 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playerinterface', '0005_auto_20210706_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='stop_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='stop_toggle',
        ),
        migrations.AddField(
            model_name='settings',
            name='play_toggle',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settings',
            name='shuffle_text',
            field=models.CharField(default='Shuffle songs', max_length=200),
        ),
        migrations.AddField(
            model_name='settings',
            name='shuffle_toggle',
            field=models.BooleanField(default=False),
        ),
    ]
