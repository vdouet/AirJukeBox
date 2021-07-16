# AirJukeBox

## I. Introduction

This project was originally designed for personal use to run on a Raspberry Pi as a background music
player for sleeping or relaxing controllable via a web interface. Support for Linux,
MacOS and Windows was added for people who want to run AirJukeBox on a computer.

AirJukeBox is a basic music player made in Python controllable using a web
interface made with Django. The original purpose of this project was to use a
Raspberry Pi connected to a stereo system (or a speaker) and to the local WiFi network to
choose which sound to play remotely (e.g. from a bed) using a web
interface accessible from anywhere in the house from the user's phone, tablet or laptop.
The main requirement was to not use the user's main device as the music player,
not use Bluetooth, and the music player should be controllable from multiple devices.


## II. Functionalities

AirJukeBox's remote functionalities include:
- Choosing which sound to play from a list of sounds stored in `Sounds/`.
- Controlling the device's sound volume.
- Setting a cutoff timer.
- Basic music player functionnalities (play, pause, stop, loop, random).
- Uploading music from the web page to the device's `Sounds/` folder to be used.
- Downloading music from YouTube to the `Sounds/` folder to be used.
- Deleting music from the `Sounds/` folder.

AirJukeBox was not originally designed to be a full-fledged music player. But feel free
to ask for (or add) new functionnalities if you want.


## III. Use cases

AirJukeBox use cases include, but are not limited to:
- Using a Raspberry Pi as a stereo receiver in your stereo sound system with the possibility to control it remotely inside your house.
- As a white noise sound machine for sleeping or relaxing.
- A background/ambient music machine.
- A basic "wireless" music player.
- Anything you can think of.


## IV. Compatibility

AirJukeBox was tested with:
- Raspberry Pi 4 using Raspberry Pi OS (32-bit) version from 2021-05-07
- MacOS Big Sur 11.0.1
- Windows 10

Ubuntu was not tested but should work. Other distributions should work fine, but amixer might need to be installed first.


## V. Requirements

AirJukeBox's requirements are:
- Python >= 3.7
- Pygame == 1.9.6 (More recent versions don't play sound on Raspberry Pi and windows).
- Django >= 3.2.5 (Tested with version 3.2.5)
- Youtube_dl >= 2021.6.6 (tested with version 2021.6.6). Install using pip!

ffmpeg or ffprobe should be installed (for YouTube-dl .ogg conversion):
- MacOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`
- Windows: https://ffmpeg.org/download.html
- Raspberry Pi: Should be included with Raspberry Pi OS.


## VI. How to use

1) Download or clone this repository.
2) Install the requirements using `pip3 install -r requirements.txt`.

- To automatically launch AirJukeBox on startup see "IX. Automatically start AirJukeBox on startup".
- You can manually start AirJukeBox using: `python3 manage.py runserver 0:8000`.


## VII. Web interface

AirJukeBox's web interface can be accessed using your device's IP on your local WiFi network followed by `:8000/playerinterface`.

Ex: `192.168.1.145:8000/playerinterface`

If you want to access the AirJukeBox's web interface from the main device you can use: `localhost:8000/playerinterface`.

## VIII. User interface

<p align="center">
<img
src="https://github.com/vdouet/AirJukeBox/blob/main/img/AirJukeBox_GUI_1.png"
alt="GUI 1" title="GUI 1" width="265" height="334"/>
<img
src="https://github.com/vdouet/AirJukeBox/blob/main/img/AirJukeBox_GUI_2.png"
alt="GUI 2" title="GUI 2" width="264" height="250"/>
</p>

AirJukeBox is a simple audio player and the user can access the following functionalities using the user interface:

- Play: Play the selected song, it will play all songs in the directory in order and the stop.
- Stop: Stop the audio player.
- Loop: Play all songs in the directory and loop back at the end.
- Random: Play all songs in the directory in random order. Can be combined with "Loop".
- Volume: Control the main device's sound volume.
- Cutoff timer: Automatically stop the audio player after the selected number of minutes. Can be enabled or disabled.
- Add song from YouTube: Download the audio from the video provided with the YouTube link and convert it to .OGG.
- Upload song: Upload a song from the user's device to the AirJukeBox 'Songs/' directory.
- Delete song: Delete a song from the 'Songs/' directory.


## IX. Automatically start AirJukeBox on startup

Tested on Raspberry Pi:

Open a terminal and copy/paste the following commands:

1) Install pm2: `wget -qO- https://getpm2.com/install.sh | bash`
2) Type: `pm2 startup`
3) Copy and paste the given command.
4) cd to AirJukeBox/AirJukeBoxSite and type: `pm2 start AirJukeBox_pm2_startup.json`
5) Type: `pm2 save`

The Django server should now launch automatically each time the Raspberry Pi starts.
On Linux and MacOS `pm2` should work in a similar way, not sure about windows.

Note: Using crontab on the Raspberry Pi caused some issues with AirJukeBox.


## X. Adding new songs

New songs can be added in three different ways:

1) Manually putting songs in the `Sounds` directory under `AirJukeBok/AirJukeBoxSite`. Songs need to be in `.mp3`, `.ogg` or `.wav` format.
2) Downloading songs from YouTube using AirJukeBox's web interface. Converting the video's audio to the `.ogg` format can take a few minutes.
3) Uploading a song directly from AirJukeBox's web interface. Songs need to be in `.mp3`, `.ogg` or `.wav` format.

Note from Pygame's documentation:
> Be aware that MP3 support is limited. On some systems an unsupported format can crash the program, e.g. Debian Linux. Consider using OGG instead.


## XI. Operating System specific volume control

AirJukeBox uses various commands to set the desired sound volume:

- Raspberry Pi / Linux: `amixer sset Master X%`
- MacOS (Darwin): `osascript -e "set Volume X"`
- Windows (Win32) using the nircmd freeware: `nircmd.exe setsysvolume X`

To get the device's sound volume:

- Raspberry Pi / Linux: `amixer sget Master`
- MacOS (Darwin): `osascript -e "set ovol to output volume of (get volume settings)"`
- Windows (Win32): No simple way was found to get the device sound volume. It will always be set at 50% after launch in AirJukeBox's inteface but can be changed after.
