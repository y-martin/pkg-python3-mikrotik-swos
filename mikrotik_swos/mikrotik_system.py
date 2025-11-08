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

RSTP_PORT_COST_MODE = {
    "short": "0x00",
    "long": "0x01" 
}

SWITCH_ID_LENGTH_MAX = 16


class Mikrotik_System(Swostab):
    def _load_tab_data(self):
        self._page = PAGE
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    # todo: iptp
    def set(self, **kwargs):
        """
        identity                          switch id
        allow_from_net4                   allowed IPv4 subnet (like 10.0.0.0/8)
        allow_from_vlan                   vlan id
        allow_from_port                   list of port index
        watchdog                          true / false
        independant_vlan_lookup           true / false
        igmp_snooping                     true / false
        igmp_fast_leave                   list of port index
        igmp_querier                      true / false (if igmp snooping enabled)
        igmp_version                      v2 / v3 
        dhcp_trusted_port                 list of port index
        dhcp_add_information_option       true / false
        mikrotik_discovery_protocol       list of port index
        rstp_bridge_priority              hex [0-ffff]
        rstp_port_cost_mode               short / long
        rsptp_forward_reserved_multicast  true / false
        
        """

        switch_id = kwargs.get("identity")
        if switch_id is not None:
            if len(switch_id) <= SWITCH_ID_LENGTH_MAX:
                self._update_data("id", utils.encode_string(switch_id))
            else:
                raise ValueError(f"switch identity length is greater than {SWITCH_ID_LENGTH_MAX}")

        allow_from_port = utils.ports_to_flag_list(kwargs.get("allow_from_port"), self.port_count)
        igmp_fast_leave = utils.ports_to_flag_list(kwargs.get("igmp_fast_leave"), self.port_count)
        dhcp_trusted_port = utils.ports_to_flag_list(kwargs.get("dhcp_trusted_port"), self.port_count)

        if kwargs.get("allow_from_net4"):
            # mikrotik switch expect a valid network/mask combination => 10.31.0.0/15 is wrong
            tokens = str(ipaddress.IPv4Network(kwargs.get("allow_from_net4"), strict=False)).split("/")
            self._update_data("alla", utils.encode_ipv4(tokens[0]))
            try:
                self._update_data("allm", utils.hex_str_with_pad(int(tokens[1]), pad=2))
            except IndexError:
                self._update_data("allm", utils.hex_str_with_pad(32, pad=2))
        if kwargs.get("allow_from_vlan"):
            self._update_data("avln", utils.hex_str_with_pad(int(kwargs.get("allow_from_vlan")), 4))
        self._update_data("allp", utils.encode_listofflags_even_len(allow_from_port))
        self._update_data("wdt", utils.encode_checkbox(kwargs.get("watchdog")))
        self._update_data("ivl", utils.encode_checkbox(kwargs.get("independant_vlan_lookup")))
        self._update_data("igmp", utils.encode_checkbox(kwargs.get("igmp_snooping")))
        self._update_data("igfl", utils.encode_listofflags_even_len(igmp_fast_leave))
        self._update_data("dtrp", utils.encode_listofflags_even_len(dhcp_trusted_port))
        self._update_data("ainf", utils.encode_checkbox(kwargs.get("dhcp_add_information_option")))

        # switch rstp is displayed in rstp tab (but GET/POST are done on sys.b)
        if kwargs.get("rstp_bridge_priority"):
            try:
                priority = int(kwargs.get("rstp_bridge_priority"), 16)
                assert(priority <= 65535)
            except (ValueError, AssertionError):
                raise ValueError("rstp_bridge_priority must be hex value in [0..ffff]")
            self._update_data("prio", utils.hex_str_with_pad(priority, pad=4))        
        self._update_data("frmc", utils.encode_checkbox(kwargs.get("rsptp_forward_reserved_multicast")))
        self._update_data("cost", RSTP_PORT_COST_MODE.get(kwargs.get("rstp_port_cost_mode", "short")))

        # 2.16 additions
        if self.version >= 2.16:
            # igmp querier
            if kwargs.get("igmp_snooping"):
                self._update_data("igmq", utils.encode_checkbox(kwargs.get("igmp_querier")))
            else:
                self._update_data("igmq", utils.encode_checkbox(False))

            # igmp version
            self._update_data("igve", IGMP_VERSION[kwargs.get("igmp_version", "v3")])

        # 2.17 additions
        if self.version >= 2.17:
            _discovery_protocol = kwargs.get("mikrotik_discovery_protocol")
            if isinstance(_discovery_protocol, bool):
                if _discovery_protocol:
                    discovery_protocol = [1] * self.port_count
                else:
                    discovery_protocol = [0] * self.port_count
            else:
                discovery_protocol = utils.ports_to_flag_list(_discovery_protocol, self.port_count)

            self._update_data("pdsc", utils.encode_listofflags_even_len(discovery_protocol))
        else:
            self._update_data("dsc", utils.encode_checkbox(kwargs.get("mikrotik_discovery_protocol")))

    def show(self):
        rstp_port_cost_mode_str = {v: k for k, v in RSTP_PORT_COST_MODE.items()}
        
        print("system tab")
        print("* version: {}" . format(self.version))
        print("* identify: {}" . format(utils.decode_string(self._data["id"])))
        print("* address acq: {}" . format(self._data["iptp"]))
        print("* address: {}" . format(utils.decode_ipv4(self._data["ip"])))
        print("* allow from: {}/{}" . format(utils.decode_ipv4(self._data["alla"]), int(self._data["allm"], 16)))
        print("* allow from vlan: {}" . format(int(self._data["avln"], 16)))
        print("* allow from ports: {}" . format(utils.decode_listofflags(self._data["allp"], self.port_count)))
        print("* watchdog: {}" . format(utils.decode_checkbox(self._data["wdt"])))
        print("* independant vlan loookup: {}" . format(utils.decode_checkbox(self._data["ivl"])))
        print("* igmp snooping: {}" . format(utils.decode_checkbox(self._data["igmp"])))
        print("* igmp fast leave: {}" . format(utils.decode_listofflags(self._data["igfl"], self.port_count)))
        print("* trusted port: {}" . format(utils.decode_listofflags(self._data["dtrp"], self.port_count)))
        print("* add information option: {}" . format(utils.decode_checkbox(self._data["ainf"])))
        print("* rstp bridge priority: {}" . format(self._data["prio"]))
        print("* rstp port cost mode: {}" . format(rstp_port_cost_mode_str[self._data["cost"]]))
        print("* rstp forward reserved multicast: {}" . format(utils.decode_checkbox(self._data["frmc"])))

        if self.version >= 2.16:
            igmp_ver_str = {v: k for k, v in IGMP_VERSION.items()}
            print("* igmp querier: {}" . format(utils.decode_checkbox(self._data["igmq"])))
            print("* igmp version: {}" . format(igmp_ver_str[self._data["igve"]]))

        if self.version >= 2.17:
            print("* mikrotik discovery protocol: {}" . format(utils.decode_listofflags(self._data["pdsc"], self.port_count)))
        else:
            print("* mikrotik discovery protocol: {}" . format(utils.decode_checkbox(self._data["dsc"])))
            
        print("")
