# Generated by Django 3.2.5 on 2021-07-05 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playerinterface', '0003_alter_settings_sound_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='play_text',
            field=models.CharField(default='Play sound', max_length=200),
        ),
        migrations.AddField(
            model_name='settings',
            name='stop_text',
            field=models.CharField(default='Stop sound', max_length=200),
        ),
        migrations.AddField(
            model_name='settings',
            name='stop_toggle',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='setting_text',
            field=models.CharField(default='Raspberry Pi audio player                                             settings', max_length=200, verbose_name='Raspberry Pi audio player settings'),
        ),
    ]