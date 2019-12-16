# DoorScheduleDisplay

Critical Making Project to send data to a Raspberry Pi Zero that gets displayed on a WaveShare 7" E-Ink display. 

## Getting Started
### Requirements: 

- Python 3 
- Install pybluez on client and server [link](https://github.com/pybluez/pybluez/blob/master/docs/install.rst)
- See [DisplayInstall](DisplayInstall.md) for instructions on setting up the E-Ink display with a Raspberry Pi Zero

### Running: 
* On the Raspberry Pi, run `python3 door_schedule_server.py`
* On your local computer, run the client `door_schedule_client` with the following options:
    - Default: Pulls and sends default schedule. Run `python3 door_schedule_client.py`
    - To Send Another Document: `python3 door_schedule_client.py doc DOC_ID_FROM_URL`
    - To Send a Picture: `python3 door_schedule_client.py image PATH_TO_IMAGE`

* NOTE: Picture functionality not finished at the moment