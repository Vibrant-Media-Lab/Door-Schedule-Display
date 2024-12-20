import time
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    for i in range(10):
        print("This device is set to power off automatically.")
        print("shutting down in " + str(100 - 10*i) + " seconds.")
        print("login as normal and type 'sudo pkill python' to interrupt")
        time.sleep(10)
        
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    print("shutdown interrupted, ")
    exit()
exit()