from sys import platform
import subprocess
import os
import re

from ..models import Settings


class Initialise_settings:
    """
    Class used to reset the settings at the start of the app.
    """

    def __init__(self):

        self.flag_initialisation = True

    def initialise_settings(self, settings: Settings):
        """Initialise all settings that should be reset at the start.

        For example we don't want to keep the name of the song played from the
        last time we used the app. We also update the volume setting using the
        device's current sound volume at launch (doesn't work on Windows).

        Args:
            settings (Settings): Django's settings model
        """

        print("Initialisation of default settings")
        settings.play_toggle = False
        settings.random_toggle = False
        settings.loop_toggle = False
        settings.song_choice = "Nothing."
        settings.volume_choice = get_sys_volume()
        settings.save()

        self.flag_initialisation = False


def to_bool(string: str) -> bool:
    """Convert a string containing either "True" or "False" to boolean.

    Args:
        string (str): The string containing either "True" or "False.

    Returns:
        bool: Return True of False
    """

    if string == 'True':
        return True
    elif string == 'False':
        return False


def change_sys_volume(vol: str) -> None:
    """Change the system sound volume using commands for various operating
    systems.

    Args:
        vol (str): The volume to set.
    """

    if platform == "linux" or platform == "linux2":
        os.system(f'amixer sset Master {vol}%')
    elif platform == "darwin":
        vol = round(int(vol) / 10)
        os.system(f'osascript -e "set Volume {vol}"')
    elif platform == "win32":
        vol = round((int(vol) / 100) * 65535)
        os.system(r"playerinterface\utils\nircmd.exe setsysvolume " +
                  str(vol))


def get_sys_volume() -> int:
    """Get the current device's system volume.

    Different commands are used various operating systems but none could be
    found for Windows.

    Returns:
        int: The system current sound volume.
    """

    if platform == "linux" or platform == "linux2":
        cmd = "amixer sget Master"
        string = subprocess.run(cmd, shell=True, capture_output=True).stdout
        result = re.search(r"\[([%-z0-9_]+)\]", str(string))
        return result.group(1).strip('%')
    elif platform == "darwin":
        cmd = 'osascript -e "set ovol to output\
            volume of (get volume settings)"'
        return int(subprocess.run(cmd, shell=True, capture_output=True).stdout)
    elif platform == "win32":
        return 50  # I did not find any way to get Windows volume.
