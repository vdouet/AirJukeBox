from multiprocessing import Process, Queue
from random import randint
from typing import Union
import pygame
import time
import os


def update_queue(q: Queue, msg: Union[str, bool]) -> None:
    """Put a new message in the multiprocessing queue for main process.

    Will check if the queue is full. If it is it will empty it first.

    Args:
        q (Queue):              The queue to put the new message in.
        msg (Union[str, bool]): The message to put in the queue.
    """

    if q.full():
        q.get()

    q.put(msg)


def lower_song_volume(mixer: pygame.mixer, cutoff_value: float = 0.05,
                      cutoff_speed: float = 0.2) -> None:
    """Lower the volume of the song rather than a sharp cutoff.

    Args:
        mixer (pygame.mixer):           To pygame mixer used to lower the
                                        volume.
        cutoff_value (float, optional): The value used to decrease the volume
                                        after each loop. Defaults to 0.05.
        cutoff_speed (float, optional): The speed used to decrease the volume.
                                        Defaults to 0.2.
    """

    volume_value = 1

    while volume_value > 0:

        volume_value -= cutoff_value
        mixer.music.set_volume(volume_value)
        time.sleep(cutoff_speed)


def song_process(rx_queue: Queue, song_name_queue: Queue,
                 play_state_queue: Queue, song_name: str, loop: bool,
                 timer_length: int, random: bool) -> None:
    """Main process for the audio player.

    Play songs and take care of the various settings set by the user such as
    loop, random, timer cutoff, etc. By default it will play each song in the
    Songs/ directory in order.

    Args:
        rx_queue (Queue):         Queue used by the main process to update
                                  settings of the audio player.
        song_name_queue (Queue):  Queue used by the audio player process to
                                  tell the main process which song is currently
                                  playing.
        play_state_queue (Queue): Queue used by the audio player process to
                                  tell the main process if it stopped playing.
        song_name (str):          The name of the song to play selected by the
                                  user in the web browser.
        loop (bool):              Used to loop or not over all the songs.
        timer_length (int):       Used to cutoff the audio player after a
                                  certain amount of time.
        random (bool):            Used to play songs in a random order or not.
    """

    terminate = False  # Stop the audio player.
    timer_count = 0  # Used to keep track of the time spent playing songs.
    sleep_time = 0.1  # Sleep value inside the loop when the player is playing.
    songs_played = 0  # Used only when random = True.
    new_song = None  # The new song to play.
    user_stop = False

    songs = sorted(os.listdir('Songs/'))  # Sorted songs in 'Songs/'.
    songs_len = len(songs) - 1

    # Initialise Pygame mixer, store it and load the specified song.
    pygame.mixer.init()
    mixer = pygame.mixer
    mixer.music.load('Songs/' + song_name)

    # If rx_queue is not empty we make sure to clear it before.
    while not rx_queue.empty():
        rx_queue.get()

    # Main player loop.
    while True and not terminate:

        # We update the current song name and play it.
        update_queue(song_name_queue, song_name)
        mixer.music.play()

        # Loop while the music is playing. We check if settings have been
        # changed, or if we should stop playing (user stop or cutoff timer).
        while mixer.music.get_busy():

            if not rx_queue.empty():

                dict = rx_queue.get()
                loop = dict.get('loop', loop)
                random = dict.get('random', random)
                timer_length = dict.get('timer', timer_length)
                terminate = dict.get('terminate', terminate)

                if terminate:
                    user_stop = True
                    lower_song_volume(mixer, 0.15, 0.1)
                    break

            time.sleep(sleep_time)
            timer_count += 1

            if timer_length and (timer_count * sleep_time) == timer_length:
                lower_song_volume(mixer)
                terminate = True
                break

        if terminate:
            break

        # If random not selected we play the song in order.
        elif not random:

            for i, song in enumerate(songs):
                if song == song_name and i < songs_len:
                    new_song = songs[i + 1]
                    mixer.music.load('Songs/' + new_song)
                    song_name = new_song
                    break
                elif i == songs_len and loop:
                    new_song = songs[0]
                    mixer.music.load('Songs/' + new_song)
                    song_name = new_song
                    break
                elif i == songs_len and not loop:
                    terminate = True
                    break

        # If random selected we choose random songs
        # (but not the same twice in a row).
        elif random:

            # If loop is not selected we terminate the player when we have
            # played all songs.
            if not loop and songs_played == songs_len:
                break

            if songs_len > 0:
                while True:
                    new_song = songs[randint(0, songs_len)]
                    if new_song != song_name:
                        break
            else:
                new_song = songs[randint(0, songs_len)]

            mixer.music.load('Songs/' + new_song)
            song_name = new_song

            if not loop:
                # Used to keep track of how many song we have played
                songs_played += 1

    # We tell the main process the audio player has stopped.
    if not user_stop:
        update_queue(play_state_queue, False)
        update_queue(song_name_queue, 'Nothing.')


class Player:
    """Class used to control the audio player process.

    Spawn the process playing songs and sending it settings set by the user in
    AirJukeBox's web page.
    """

    def __init__(self) -> None:

        self.process = None
        self.tx_queue = Queue()
        self.song_name_queue = Queue(maxsize=1)
        self.play_state_queue = Queue(maxsize=1)

    def play_song(self, song_name: str, loop: bool, timer_time: str,
                  istimer: bool, random: bool) -> None:
        """Spawn the audio player process

        It will first check if the audio player process is alive, if yes, it
        will send a command to terminate it.

        Args:
            song_name (str):  Song to play selected by the user.
            loop (bool):      If the loop setting is activated or not.
            timer_time (str): The time used by the cutoff timer.
            istimer (bool):   If the timer setting is activated or not.
            random (bool):    If the random setting is activated or not.
        """

        if self.process and self.process.is_alive():
            self.tx_queue.put({"terminate": True})

        # If timer is activated or timer time setting is 0 we don't activate
        # the timer. Else we convert the time value from minutes to seconds.
        if not istimer or int(timer_time) == 0:
            timer_time = None
        else:
            timer_time *= 60

        self.process = Process(target=song_process,
                               args=(self.tx_queue, self.song_name_queue,
                                     self.play_state_queue, song_name, loop,
                                     timer_time, random))

        self.process.start()

    def stop_song(self) -> None:
        """Send a terminate command to the audio player process by putting it
        in the tx queue.
        """

        if self.process and self.process.is_alive():
            self.tx_queue.put({"terminate": True})

    def change_loop(self, loop: bool) -> None:
        """Update the loop setting in the audio player process by sending it
        the new value in the tx queue.

        Args:
            loop (bool): If the loop setting is activated or not.
        """

        if self.process and self.process.is_alive():
            self.tx_queue.put({"loop": loop})

    def change_random(self, random: bool) -> None:
        """Update the random setting in the audio player process by sending it
        the new value in the tx queue.

        Args:
            random (bool): If the random setting is activated or not.
        """

        if self.process and self.process.is_alive():
            self.tx_queue.put({"random": random})

    def change_timer(self, istimer: bool, timer_time: str) -> None:
        """Update the timer setting in the audio player process by sending it
        the new value in the tx queue.

        Args:
            istimer (bool):   If the timer setting is activated or not.
            timer_time (str): The time selected for the timer cutoff.
        """

        if self.process and self.process.is_alive():
            if istimer and int(timer_time) > 0:
                self.tx_queue.put({"timer": int(timer_time) * 60})
            elif not istimer or int(timer_time) == 0:
                self.tx_queue.put({"timer": None})
