# DoorScheduleDisplay

Critical Making Project to send data to a Raspberry Pi Zero that gets displayed on a WaveShare 7" E-Ink display. 

## Getting Started
### Requirements: 

- Python 3 
- [Install pybluez](https://github.com/pybluez/pybluez/blob/master/docs/install.rst) on client and server
- See [DisplayInstall](DisplayInstall.md) for instructions on setting up the E-Ink display with a Raspberry Pi Zero

### Notes on installation and running: 
- You may have to run the scripts as sudo if a permission denied error occurs.
- On Linux, you may have to run Bluetooth in compatibility mode. If that occurs, see [here](https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory/46810116) and reboot.

### Running: 
* On the Raspberry Pi, run `python3 door_schedule_server.py`
* On your local computer, run the client `door_schedule_client` with the following options:
    - Default: Pulls and sends default schedule. Run `python3 door_schedule_client.py`
    - To Send Another Document: `python3 door_schedule_client.py doc DOC_ID_FROM_URL`
    - To Send a Picture: `python3 door_schedule_client.py image PATH_TO_IMAGE`

* NOTE: Picture functionality not finished at the moment