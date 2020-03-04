# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14
# Adapted for Python3 by Michael duPont 2015-04-05

# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"

#Installation
#sudo apt-get install libbluetooth-dev bluez
#sudo pip-3.2 install pybluez   #pip-3.2 for Python3.2 on Raspberry Pi

import os
import struct
import sys

import bluetooth._bluetooth as bluez

LE_META_EVENT = 0x3e
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_ENABLE=0x000C

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02

def getBLESocket(devID):
	return bluez.hci_open_dev(devID)

def number_packet(pkt):
    # b'\x89='
    myInteger = 0
    multiple = 256
    for i in range(len(pkt)):
        # 35072
        # 61
        myInteger += struct.unpack("B",pkt[i:i+1])[0] * multiple
        multiple = 1
    return myInteger # 35133

def string_packet(pkt):
    #  UUID is 16 Bytes
    # b'\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    # so len() is 16
    # loop over each byte, get it to hex, build up the string (uuid is 32 chars, 16bytes)
    myString = "";
    for i in range(len(pkt)):  # 0-16 loop
        myString += "%02x" %struct.unpack("B",pkt[i:i+1])[0]
    return myString

def packed_bdaddr_to_string(bdaddr_packed):
    #  iBeacon packets have the mac byte-reversed, reverse with bdaddr_packed[::-1]
    #  b'ID\x8b\xea&b' -> b'b&\xea\x8bDI'
    #  decode to int -> (98, 38, 234, 139, 68, 73) , join by : as hex -> '62:26:ea:8b:44:49'
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def hci_le_set_scan_parameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

def parse_events(sock, loop_count=100):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    beacons = []
    for i in range(0, loop_count):
        pkt = sock.recv(255)
        # http://www.havlena.net/wp-content/themes/striking/includes/timthumb.php?src=/wp-content/uploads/ibeacon-packet.png&w=600&zc=1
        #pkt = b'\x04>+\x02\x01\x03\x01r\xed\x08S\x84=\x1f\x1e\xff\x06\x00\x01\t \x02)\xa7\x93\xe2\xfdD\x1b\xafhOH\xef>mn\x91\xcb\x14\x02$\x98\xc7\xef\xb3'
        #       |      |   |   |   |    |             |                                   |                                          |     |              |
        #       | event|sub|#rep\  |    |  mac addr   |                                   |    uuid                                  | major\ minor|      |
        ptype, event, plen = struct.unpack("BBB", pkt[:3])  # b'\x04>(' -> (4, 62, 40)
        if event == LE_META_EVENT:  # 62 -> 0x3e -> HCI Event: LE Meta Event (0x3e) plen 39
            subevent, = struct.unpack("B", pkt[3:4]) # b'\x02' -> (2,)
            # chop off \x04>+\x02 (the event + subevent)
            pkt = pkt[4:]  # b'\x01\x03\x01r\xed\x08S\x84=\x1f\x1e\xff\x06\x00\x01\t \x02)\xa7\x93\xe2\xfdD\x1b\xafhOH\xef>mn\x91\xcb\x14\x02$\x98\xc7\xef\xb3'
            if subevent == EVT_LE_ADVERTISING_REPORT:  # if 0x02 (2) -> all iBeacons use this
                num_reports = struct.unpack("B", pkt[0:1])[0]  # b'\x01' -> (1,) -> number of reports to receive
                for i in range(0, num_reports):
                    # build the return string
                    beacons.append({
                        'mac': packed_bdaddr_to_string(pkt[3:9]),  #  b'r\xed\x08S\x84='
                        'uuid': string_packet(pkt[22:6]),    #  b'\x93\xe2\xfdD\x1b\xafhOH\xef>mn\x91\xcb\x14'
                        'minor': number_packet(pkt[4:2]),    #  b'\x98\xc7'
                        'major': number_packet(pkt[6:4]),    #  b'\x02$'
                    })
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return beacons
