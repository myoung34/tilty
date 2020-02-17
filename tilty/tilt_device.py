# -*- coding: utf-8 -*-
""" Class to represent the actual device """

from datetime import datetime

import bluetooth._bluetooth as bluez

from tilty import blescan, constants


class TiltDevice:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, device_id=0):
        """ Initializer

        Args:
            device_id: (int) represents the device id for HCI
            sock: the socket to open
        """
        self.sock = bluez.hci_open_dev(device_id)

    def start(self):
        """ Start scanning and device

        Args:
        """
        blescan.hci_le_set_scan_parameters(self.sock)
        blescan.hci_enable_le_scan(self.sock)

    def stop(self):
        """ Stop scanning and device

        Args:
        """
        blescan.hci_disable_le_scan(self.sock)

    def scan_for_tilt_data(self):
        """ scan for tilt and return data if found """

        data = None
        for beacon in blescan.parse_events(self.sock, 10):
            if beacon['uuid'] in constants.TILT_DEVICES:
                data = {
                    'color': constants.TILT_DEVICES[beacon['uuid']],
                    'gravity': beacon['minor'],
                    'temp': beacon['major'],
                    'timestamp': datetime.now().isoformat(),
                }

        return data
