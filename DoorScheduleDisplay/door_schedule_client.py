#!/usr/bin/env python3

import sys
import bluetooth

# google docs api interface
from document_interface import * 

class DoorScheduleSender(object): 
    def __init__(self, addr_pi):
        print("Searching for Pi service...")
        self.sock = self._connect_server(addr_pi)
        if self.sock is None: 
            raise RuntimeError("ERROR: cannot connect to server")

    def _connect_server(self, addr): 
        # search for the right service
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        service_matches = bluetooth.find_service(uuid=uuid, address=addr)

        if len(service_matches) == 0:
            print("Couldn't find the service.")
            return None

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"].decode()

        print("Connecting to \"{}\" on {}".format(name, host))

        # Create the client socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((host, port))

        return sock

    def send_data(self, data):
        try: 
            self.sock.send(str.encode(data))
        except Exception: 
            print("ERROR: exception sending over socket")
            self.cleanup()
            raise

    def cleanup(self): 
        self.sock.close()

def main():
    # TODO: copy Pi mac address here
    addr_pi = "MAC_ADDR_HERE"

    if len(sys.argv) < 2:
        # default mode
        DOCUMENT_ID = '1nwFP7-tiCmU3g6_ctxyhKiiuLuDDl9KTs9k8T1UO_Lc'
        client = DoorScheduleSender(addr_pi)
        
        try: 
            lines = "\n".join(get_doc(DOCUMENT_ID).split('\n')[3:8])
        except Exception: 
            print("ERROR: exception retrieving lines from Google Doc")
            client.cleanup()
            raise

        client.send_data(lines)
        print("Successfully sent Google Doc to Pi")
    elif sys.argv[1].strip() == "doc":
        if len(sys.argv) < 3:
            print("ERROR: too few arguments for custom document")
            print_usage()
            sys.exit(0)
        else:
            DOCUMENT_ID = sys.argv[2].strip()

            try: 
                lines = "\n".join(get_doc(DOCUMENT_ID).split('\n')[3:8])
            except Exception: 
                print("ERROR: exception retrieving lines from Google Doc")
                client.cleanup()
                raise

            client = DoorScheduleSender(addr_pi)
            client.send_data(lines)
            print("Successfully sent Google Doc {} to Pi".format(DOCUMENT_ID))

    elif sys.argv[1].strip() == "image":
        if len(sys.argv) < 3:
            print("ERROR: too few arguments for sending image")
            print_usage()
            sys.exit(0)
        else:
            print("Still need to implement sending image to Pi")
    else: 
        print("ERROR: invalid arguments")
        print_usage()

def print_usage(): 
    buf = "DoorScheduleClient usage: \n" + \
          "\tDefault: run `python3 door_schedule_client.py` \n" + \
          "\tTo Send Another Document: `python3 door_schedule_client.py doc DOC_ID_FROM_URL` \n" + \
          "\tTo Send a Picture: `python3 door_schedule_client.py image PATH_TO_IMAGE` \n"
    print(buf)

if __name__ == "__main__": 
    main()
