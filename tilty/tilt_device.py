# -*- coding: utf-8 -*-
""" Class to represent the actual device """

from datetime import datetime

import bluetooth._bluetooth as bluez

from tilty import blescan, constants
from tilty.tilty import LOGGER


class TiltDevice:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, device_id: int = 0) -> None:
        """ Initializer

        Args:
            device_id: (int) represents the device id for HCI
            sock: the socket to open
        """
        LOGGER.debug('Opening device socket')
        self.sock = bluez.hci_open_dev(device_id)

    def start(self) -> None:
        """ Start scanning and device

        Args:
        """
        LOGGER.debug('Setting scan parameters and enabling LE scan')
        blescan.hci_le_set_scan_parameters(self.sock)
        blescan.hci_enable_le_scan(self.sock)

    def stop(self) -> None:
        """ Stop scanning and device

        Args:
        """
        LOGGER.debug('Stopping device socket')
        blescan.hci_disable_le_scan(self.sock)

    def scan_for_tilt_data(self) -> list:
        """ scan for tilt and return data if found """

        data = []
        LOGGER.debug('Looking for events')
        for beacon in blescan.get_events(self.sock):
            uuid = beacon.get('uuid')
            if uuid is None:
                continue
            color = constants.TILT_DEVICES.get(uuid)
            if color:
                data.append({
                    'color': color,
                    'gravity': float(beacon['minor']/1000),
                    'temp': beacon['major'],
                    'mac': beacon['mac'],
                    'timestamp': datetime.now().isoformat(),
                    'uuid': uuid
                })
            else:
                LOGGER.debug(
                    "Beacon UUID is not a tilt device: %s",
                    uuid
                )

        return data
