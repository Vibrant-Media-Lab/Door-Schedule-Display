#!/usr/bin/env python3

import time
import bluetooth
import traceback

from display_driver import DisplayDriver

class DoorScheduleServer(object): 
    def __init__(self): 
        print("Server starting up...")
        self._server_sock = self._start_bt_server()

        self._disp_driver = DisplayDriver()        

    def _start_bt_server(self):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service(server_sock, 
                                    "SampleServer", 
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                    )
        return server_sock

    def main(self):
        while True: 
            try: 
                data = self.accept_connections()
                if data is not None: 
                    success = self._disp_driver.display_data(data)
                    print("Success in displaying data: {}".format(success))

                # update every second
                time.sleep(1)
            except Exception: 
                print("ERROR: Exception occurred while running")
                print(traceback.format_exc())
                raise

    def cleanup(self):
        self._server_sock.close()

    def accept_connections(self): 
        print("Waiting for connection...")
        client_sock, client_info = self._server_sock.accept()
        print("Accepted connection from {}".format(client_info))

        try:
            data = client_sock.recv(1024)
            if data is None: 
                return None
            print("Received {} bytes".format(len(data)))
            return data.decode()
        except IOError:
            return None
        finally: 
            client_sock.close()

if __name__ == "__main__": 
    server = DoorScheduleServer()
    server.main()
