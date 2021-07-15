from queue import Empty
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from playerinterface.utils.audioplayer import Player
from django.core.handlers.wsgi import WSGIRequest
from playerinterface.utils.utils import Initialise_settings, to_bool
from playerinterface.utils.utils import change_sys_volume
from youtube_dl import YoutubeDL
from django.urls import reverse
import os

from .models import Settings

player = Player()
init = Initialise_settings()


def index(request: WSGIRequest) -> HttpResponse:
    """Index view

    Initialise default settings at launch, update current song's name and play
    state each time if available.

    Args:
        request (WSGIRequest): Request from the main web page.

    Returns:
        HttpResponse: Django Http response.
    """

    settings = Settings.objects.all()[0]

    if init.flag_initialisation:
        init.initialise_settings(settings)

    if not player.song_name_queue.empty():
        try:
            settings.song_choice = player.song_name_queue.get(timeout=1)
        except Empty:
            settings.song_choice = "Nothing."
        settings.save()

    if not player.play_state_queue.empty():
        settings.play_toggle = player.play_state_queue.get(timeout=1)
        settings.save()

    context = {
        'settings': settings,
        'songs_list': sorted(os.listdir('Songs/')),
    }

    return render(request, 'playerinterface/index.html', context)


def change_timer(request: WSGIRequest,
                 settings_id: int) -> HttpResponseRedirect:
    """Change the cutoff timer of the audio player.

    Args:
        request (WSGIRequest): Request from the main web page.
        settings_id (int): Current settings ID from the Settings model.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    settings = get_object_or_404(Settings, pk=settings_id)
    settings.timer_choice = request.POST.get('timer', settings.timer_choice)
    settings.timer_toggle = to_bool(request.POST['toggle_timer'])
    settings.save()

    player.change_timer(settings.timer_toggle, settings.timer_choice)

    return HttpResponseRedirect(reverse('playerinterface:index'))


def change_random(request: WSGIRequest,
                  settings_id: int) -> HttpResponseRedirect:
    """Activate or deactivate the random setting in the audio player.

    Args:
        request (WSGIRequest): Request from the main web page.
        settings_id (int): Current settings ID from the Settings model.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    settings = get_object_or_404(Settings, pk=settings_id)

    # No need to check toggle_random value, it should always contain
    # something. We just use it as a toggle.
    if request.POST['toggle_random']:
        settings.random_toggle = not settings.random_toggle

    player.change_random(settings.random_toggle)

    settings.save()

    return HttpResponseRedirect(reverse('playerinterface:index'))


def change_play(request: WSGIRequest,
                settings_id: int) -> HttpResponseRedirect:
    """Play or stop the audio player.

    Args:
        request (WSGIRequest): Request from the main web page.
        settings_id (int): Current settings ID from the Settings model.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    settings = get_object_or_404(Settings, pk=settings_id)

    settings.song_choice = request.POST['song']

    if 'Play' in request.POST['toggle_play']:
        settings.play_toggle = True
        player.play_song(settings.song_choice, settings.loop_toggle,
                         settings.timer_choice, settings.timer_toggle,
                         settings.random_toggle)

    elif 'Stop' in request.POST['toggle_play']:
        # We need empty the song name queue.
        if not player.song_name_queue.empty():
            try:
                player.song_name_queue.get(timeout=1)
            except Empty:
                pass
        settings.play_toggle = False
        player.stop_song()
        settings.song_choice = "Nothing."

    settings.save()

    return HttpResponseRedirect(reverse('playerinterface:index'))


def change_volume(request: WSGIRequest,
                  settings_id: int) -> HttpResponseRedirect:
    """Change the system sound volume.

    Args:
        request (WSGIRequest): Request from the main web page.
        settings_id (int): Current settings ID from the Settings model.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    settings = get_object_or_404(Settings, pk=settings_id)
    settings.volume_choice = request.POST['volume']
    settings.save()

    change_sys_volume(settings.volume_choice)

    return HttpResponseRedirect(reverse('playerinterface:index'))


def change_loop(request: WSGIRequest,
                settings_id: int) -> HttpResponseRedirect:
    """Activate or deactivate the loop settings from the audio player.

    Args:
        request (WSGIRequest): Request from the main web page.
        settings_id (int): Current settings ID from the Settings model.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    settings = get_object_or_404(Settings, pk=settings_id)

    # No need to check toggle_loop value, it should always contain
    # something. We just use it as a toggle.
    if request.POST['toggle_loop']:
        settings.loop_toggle = not settings.loop_toggle

    settings.save()

    player.change_loop(settings.loop_toggle)

    return HttpResponseRedirect(reverse('playerinterface:index'))


def download_youtube(request: WSGIRequest) -> HttpResponseRedirect:
    """Download song from youtube and convert it in OGG format.

    Args:
        request (WSGIRequest): Request from the main web page.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    ytdl_options = {
        'format': 'bestaudio/best',
        'outtmpl': 'Songs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ytdl_options) as youtube_song:
        youtube_song.extract_info(request.POST['youtube_url'])

    return HttpResponseRedirect(reverse('playerinterface:index'))


def upload_song(request: WSGIRequest) -> HttpResponseRedirect:
    """Upload a song from the web page to the 'Songs/' directory.

    Args:
        request (WSGIRequest): Request from the main web page.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    path = "Songs/" + str(request.FILES['song_to_upload'])
    print(path)

    with open(path, 'wb+') as destination:
        for chunk in request.FILES['song_to_upload'].chunks():
            destination.write(chunk)

    return HttpResponseRedirect(reverse('playerinterface:index'))


def delete_song(request: WSGIRequest) -> HttpResponseRedirect:
    """Delete a song from the 'Songs/' directory.

    Args:
        request (WSGIRequest): Request from the main web page.

    Returns:
        HttpResponseRedirect: Redirection to the index page.
    """

    path = "Songs/" + request.POST['song']
    if os.path.exists(path):
        os.remove(path)
    else:
        print("path not found.")

    return HttpResponseRedirect(reverse('playerinterface:index'))
