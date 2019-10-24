# Set up Pi Zero
## Configure Pi
Open terminal, use command to enter the configuration page  
``` sudo raspi-config ```  
Choose `Interfacing Options -> SPI -> Yes`  to enable SPI interface  
RPI open spi.png

Reboot Raspberry Pi：
``` sudo reboot ```  
Please make sure that SPI interface was not used by other device

## Libraries Installation
### Install BCM2835 libraries
``` wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz ```  
``` tar zxvf bcm2835-1.60.tar.gz ```  
``` cd bcm2835-1.60/ ```  
``` sudo ./configure ```  
``` sudo make ```  
``` sudo make check ```  
``` sudo make install ```  
``` #For more details, please refer to http://www.airspayce.com/mikem/bcm2835/ ```  
``` Install wiringPi libraries ```  
``` sudo apt-get install wiringpi ```  

``` #For Pi 4, you need to update it：```  
``` cd /tmp ```  
``` wget https://project-downloads.drogon.net/wiringpi-latest.deb ```    
``` sudo dpkg -i wiringpi-latest.deb ```    
``` gpio -v ```   
``` #You will get 2.52 information if you install it correctly ```   

## Install Python libraries
``` #python2 ```  
``` sudo apt-get update ```    
``` sudo apt-get install python-pip ```   
``` sudo apt-get install python-pil ```    
``` sudo apt-get install python-numpy ```    
``` sudo pip install RPi.GPIO ```    
``` sudo pip install spidev ```  

``` #python3 ```     
``` sudo apt-get update ```    
``` sudo apt-get install python3-pip ```     
``` sudo apt-get install python3-pil ```    
``` sudo apt-get install python3-numpy ```    
``` sudo pip3 install RPi.GPIO ```    
``` sudo pip3 install spidev ```    

## Download examples
Open terminal and execute command to download demo codes  
``` sudo git clone https://github.com/waveshare/e-Paper ```   
``` cd e-Paper/RaspberryPi\&JetsonNano/ ```    


Open up the python terminal  
` python `  
Run examples, xxx is the name of the e-Paper. For example, if you want to run codes of 1.54inch e-Paper Module, you xxx should ` be epd_1in54 `  
` cd python/examples ` 
` #python2 `  
` sudo python xxx.py `  
` #python3 `  
` sudo python3 xxx.py `  
