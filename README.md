# DoorScheduleDisplay

Critical Making Project to send data to a Raspberry Pi Zero that gets displayed on a WaveShare 7" E-Ink display. 

## Getting Started
### Requirements: 

- Python 3 
- [Install pybluez](https://github.com/pybluez/pybluez/blob/master/docs/install.rst) on client and server
    - You might also have to install [lightblue](https://pypi.org/project/python-lightblue/) on client and server
    - NOTE: both these libraries are not supported anymore and there are a lot of possible bugs suring the installation or the use of the libraries that might not let you run the scripts. Another library to consider if that happens is [BlueDot](https://bluedot.readthedocs.io/en/latest/gettingstarted.html), however that will force you to have to change the scripts and this library relies on others that aren't supported anymore which might cause problems.
- You might have to install the https://pypi.org/project/google-api-python-client/ to get the scripts to work as well.
- See [DisplayInstall](DisplayInstall.md) for instructions on setting up the E-Ink display with a Raspberry Pi Zero

### Notes on installation and running: 
- You may have to run the scripts as sudo if a permission denied error occurs.
- On Linux, you may have to run Bluetooth in compatibility mode. If that occurs, see [here](https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory/46810116) and reboot.

### Running: 
* Connect raspberry pi to wifi (ideally the same one that the client from which we will access the document is connected to)
* Go through the server and client scripts and make sure to change the UUID and MAC addresses that match your pi.
* On the Raspberry Pi, run `python3 door_schedule_server.py`
* NOTE: if you get 'bluetooth.btcommon.BluetoothError: no advertisable device' error you will have to open the ports on your pi. Here is a [link](https://www.youtube.com/watch?v=vpyQooUksBk) on how to do it.
* On your local computer, run the client `door_schedule_client` with the following options:
    - Default: Pulls and sends default schedule. Run `python3 door_schedule_client.py`
    - To Send Another Document: `python3 door_schedule_client.py doc DOC_ID_FROM_URL`
    - To Send a Picture: `python3 door_schedule_client.py image PATH_TO_IMAGE`

* NOTE: Picture functionality not finished at the moment
* NOTE: As of now, there are problems trying to connect the bluetooth server and client which have not been solved yet.
