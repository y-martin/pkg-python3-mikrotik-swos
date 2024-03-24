#!/usr/bin/env python3


import ipaddress

from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# snmp payload
# {iptp:0x01,ip:0xfa001f0a,id:'4d696b726f54696b',alla:0x00,allm:0x00,allp:0xc00003,avln:0x044c,wdt:0x01,ivl:0x00,igmp:0x01,igfl:0x01020000,dsc:0x00,dtrp:0x01c20000,ainf:0x01,ver:'322e3133'}
PAGE = "/sys.b"


IGMP_VERSION = {
    "v2": "0x00",
    "v3": "0x01"
}


class Mikrotik_System(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    # todo: iptp
    def set(self, **kwargs):
        if kwargs.get("allow_from_net4", None):
            # mikrotik switch expect a valid network/mask combination => 10.31.0.0/15 is wrong
            tokens = str(ipaddress.IPv4Network(kwargs.get("allow_from_net4"), strict=False)).split("/")
            self._update_data("alla", utils.encode_ipv4(tokens[0]))
            try:
                self._update_data("allm", utils.hex_str_with_pad(int(tokens[1]), pad=2))
            except IndexError:
                self._update_data("allm", utils.hex_str_with_pad(32, pad=2))
        if kwargs.get("allow_from_vlan", None):
            self._update_data("avln", utils.hex_str_with_pad(int(kwargs.get("allow_from_vlan")), 4))
        self._update_data("allp", utils.encode_listofflags(kwargs.get("allow_from_port", None), 8))
        self._update_data("wdt", utils.encode_checkbox(kwargs.get("watchdog", None)))
        self._update_data("ivl", utils.encode_checkbox(kwargs.get("independant_vlan_lookup", None)))
        self._update_data("igmp", utils.encode_checkbox(kwargs.get("igmp_snooping", None)))
        self._update_data("igfl", utils.encode_listofflags(kwargs.get("igmp_fast_leave", None), 8))
        self._update_data("dsc", utils.encode_checkbox(kwargs.get("mikrotik_discovery_protocol", None)))
        self._update_data("dtrp", utils.encode_listofflags(kwargs.get("dhcp_trusted_port", None), 8))
        self._update_data("ainf", utils.encode_checkbox(kwargs.get("dhcp_add_information_option", None)))
        self._update_data("id", utils.encode_string(kwargs.get("identity", None)))

        # 2.16 additions
        if self.version >= 2.16:
            # igmp querier
            if kwargs.get("igmp_snooping", None):
                self._update_data("igmq", utils.encode_checkbox(kwargs.get("igmp_querier", None)))
            else:
                self._update_data("igmq", utils.encode_checkbox(False))

            # igmp version
            self._update_data("igve", IGMP_VERSION[kwargs.get("igmp_version", "v3")])
        
        return self._save(PAGE)

    def show(self):
        print("system tab")
        print("* version: {}" . format(self.version))
        print("* identify: {}" . format(utils.decode_string(self._data["id"])))
        print("* address acq: {}" . format(self._data["iptp"]))
        print("* address: {}" . format(utils.decode_ipv4(self._data["ip"])))
        print("* allow from: {}/{}" . format(utils.decode_ipv4(self._data["alla"]), int(self._data["allm"], 16)))
        print("* allow from vlan {}" . format(int(self._data["avln"], 16)))
        print("* allow from ports {}" . format(utils.decode_listofflags(self._data["allp"], self.port_count)))
        print("* watchdog {}" . format(utils.decode_checkbox(self._data["wdt"])))
        print("* independant vlan loookup {}" . format(utils.decode_checkbox(self._data["ivl"])))
        print("* igmp snooping {}" . format(utils.decode_checkbox(self._data["igmp"])))
        print("* igmp fast leave {}" . format(utils.decode_listofflags(self._data["igfl"], self.port_count)))
        print("* mikrotik discovery protocol {}" . format(utils.decode_checkbox(self._data["dsc"])))
        print("* trusted port {}" . format(utils.decode_listofflags(self._data["dtrp"], self.port_count)))
        print("* add information option {}" . format(utils.decode_checkbox(self._data["ainf"])))

        if self.version >= 2.16:
            igmp_ver_str = {v: k for k, v in IGMP_VERSION.items()}
            
            print("* igmp querier {}" . format(utils.decode_checkbox(self._data["igmq"])))
            print("* igmp version {}" . format(igmp_ver_str[self._data["igve"]]))

        print("")
