# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-function-docstring
""" This Module parses iBeacon events for the tilt hydrometer """
import struct

import bluetooth._bluetooth as bluez


def get_socket(device_id):
    return bluez.hci_open_dev(device_id)


def string_packet(pkt):
    #  UUID is 16 Bytes
    # b'\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    # so len() is 16
    # loop over each byte, get it to hex, build up the string (uuid is 32 chars, 16bytes)  # noqa
    return ''.join(["%02x" % int.from_bytes(pkt[i:i+1], "big") for i in range(len(pkt))])  # noqa


def packed_bdaddr_to_string(bdaddr_packed):
    #  iBeacon packets have the mac byte-reversed, reverse with bdaddr_packed[::-1]  # noqa
    #  b'ID\x8b\xea&b' -> b'b&\xea\x8bDI'
    #  decode to int -> (98, 38, 234, 139, 68, 73) , join by : as hex -> '62:26:ea:8b:44:49'  # noqa
    return ':'.join('%02x' % i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))  # noqa


def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)


def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)


def hci_toggle_le_scan(sock, enable):
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, 0x08, 0x000C, cmd_pkt)


def hci_le_set_scan_parameters(sock):
    sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)


def get_events(sock, loop_count=100):
    old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)
    beacons = []
    for i in range(0, loop_count):  # pylint: disable=unused-variable
        pkt = sock.recv(255)
        beacons.append(parse_packet(pkt))
    sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)
    return beacons


def parse_packet(pkt):
    # http://www.havlena.net/wp-content/themes/striking/includes/timthumb.php?src=/wp-content/uploads/ibeacon-packet.png&w=600&zc=1
    #pkt = b'   \x04>*                      \x02\x01x03\x01w\t  \xbc\xd0W\xef\x1e\x02\x01\x04\x1a\xffL\x00\x02\x15    \xa4\x95\xbb0\xc5\xb1KD\xb5\x12\x13p\xf0-t\xde  \x00B  \x03\xf7   \xc5\xa7'   # noqa
    #       |                  |           |                   |                                                    |                                                |      |         |          |  # noqa
    #       | preamble+header  |                         PDU                                                                                                                                     |  # noqa
    #       |     3 bytes      |                        x bytes (plen)                                                                                                                           |  # noqa
    #       |                  |           |    mac addr       |           uuid                                     |          unused data                           | major| minor   |   tx     |  # noqa
    #       |                  |           |                   |                                                    |                                                | temp | gravity |          |  # noqa
    ptype, event, plen = struct.unpack("BBB", pkt[:3])  # b'\x04>+' -> (4, 62, 40)  # pylint:disable=unused-variable  # noqa
    if event == 0x3e:  # 62 -> 0x3e -> HCI Event: LE Meta Event (0x3e) plen 44
        subevent, = struct.unpack("B", pkt[3:4])  # b'\x02' -> (2,)
        if subevent == 0x02:  # if 0x02 (2) -> all iBeacons use this
            return {
                'mac': packed_bdaddr_to_string(pkt[3:9]),   # mac   -> 6 bytes -> b'\x02\x01\x03\x01w\t'  # noqa
                'uuid': string_packet(pkt[-22:-6]),         # uuid  -> 16bytes -> b'\xa4\x95\xbb0\xc5\xb1KD\xb5\x12\x13p\xf0-t\xde'  # noqa
                'major': int.from_bytes(pkt[-6:-4], "big"), # major -> 2 bytes -> b'\x00B'  # noqa
                'minor': int.from_bytes(pkt[-4:-2], "big"), # minor -> 2 bytes -> b'\x03\xf7'  # noqa
            }
    return {}
