# DoorScheduleDisplay

Critical Making Project to send data to a Raspberry Pi Zero that gets displayed on a WaveShare 7" E-Ink display. 

## Getting Started

### Notes from the Fall 2024 group:
- Logistics:
    - Pi Username: vml | Password: eink
    - We decided to completely reinstall the pi OS as it was running incredibly slowly and we were unable to SSH into it. We decided against Linux with GUI as it was running incredibly slowly
    - Unfortunately, we were unable to connect the pi to PittNet or PITT-MDA. We used phone hotspots to SSH into the pi.
    - Due to lack of Linux experience, we held off of scheduling the pi to run the appropriate scripts on boot. During testing, we had trouble and decided it would be better for someone with more Linux experience to set it up instead
- Packages:
    - Similarly to the Fall 2023 group, we installed the appropriate packages and dependencies by following the manufacturer's tutorial.
    - Aside from standard Python libraries, this project used the BeautifulSoup4 library to parse HTML from the VML schedule document, as well as PIL to generate the images for the display.
- Aside from finishing up the networking and automation of all necessary scripts to run sequentially, there are a few improvements that could be made, such as:
    - Integrating the button that is connected to the housing as some sort of wake/refresh button. This might require soldering to the board in order to function while the pi is truly powered off
    - Making a new housing/casing for the whole display, as the current one has a few quirks (such as the ribbon cable sticking out of the bottom and the screen and pi not being fixed to the case)
    - Improving/restructuring the code, such as:
        - Abstracting certain sections into separate functions
        - Using terminal/command line input for params rather than global variables declared at the start of the script. 
        - Combine the various scripts into one script that executes all parts of the process
    - Testing generalizability with other screens/screen sizes, exploring other e-ink display applications, etc.

### Notes From The Fall 2023 Project Group: 
* SSH
    - IP: for us it was 172.20.10.9, but you can use the command "ifconfig" to view the IP under "inet"
      - ssh into raspberry pi from external computer: ssh pi@172.20.10.9
    - Username: pi
    - Password: einkpi
* In the home directory of the Raspberry Pi, there are two main directories
    - e-Paper: we created this by following this tutorial from start to finish https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi. It has all the test files that should display               something to the E-Ink display.
    - Door-Schedule-Display: the starter code left for us by the previous group, but we couldn't figure out how to run and make it work.
 * Outcome of e-Paper directory:
    - we got to the part of the tutorial where you run the code (C or Python) to send an image to the e-ink display. The diplay ended up drawing two horizontal lines, and nothing else, and thats as far as we got.
* New Code added:
    - we added the folder Fall2023DoorScheduleDisplay. In there, you'll find client and server code as well as a web scraper that scrapes the VML's website and gives you the hours hopefully, you'll be able to use             this to proceed with the project. There is also starter code for a client and server if you choose to go down that path, but we decided not to as the pi can be connected to wifi by itself and scrape the                information on its own without any client helping it.


### Requirements (prior to Fall 2023): 

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
