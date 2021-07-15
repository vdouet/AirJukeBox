from django.db import models


class Settings(models.Model):
    """Django model

    Contain all settings for the audio player.

    Args:
        models (Model): Django model
    """
    setting_text = models.CharField("Audio player settings",
                                    max_length=200,
                                    default="Audio player settings")

    volume_text = models.CharField(default="Volume", max_length=200)
    volume_choice = models.IntegerField(default=0)

    loop_text = models.CharField(default="Loop song", max_length=200)
    loop_toggle = models.BooleanField(default=True)

    timer_text = models.CharField(default="Cutoff timer", max_length=200)
    timer_toggle = models.BooleanField(default=False)
    timer_choice = models.IntegerField(default=0)

    song_text = models.CharField(default="Select song to play",
                                 max_length=200)
    song_choice = models.CharField(blank=True,
                                   null=True,
                                   default=None,
                                   max_length=200)

    play_text = models.CharField(default="Play song", max_length=200)
    play_toggle = models.BooleanField(default=False)

    random_text = models.CharField(default="random songs", max_length=200)
    random_toggle = models.BooleanField(default=False)

    def __str__(self):
        return self.setting_text
