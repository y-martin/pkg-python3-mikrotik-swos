#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# {en:0x03c20007,nm:['6d657a7a5f6c6170746f70','6d657a7a5f67616d65','627572656175','506f727434','506f727435','506f727436','506f727437','506f727438','506f727439','506f72743130','506f72743131','506f72743132','506f72743133','506f72743134','506f72743135','506f72743136','506f72743137','6e6574','506f72743139','506f72743230','506f72743231','506f72743232','6865795f31','6865795f32','53465031','53465032'],an:0x03ffffff,spdc:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01],dpxc:0x03ffffff,fctc:0x03ffffff,fctr:0x03ffffff}
PAGE = "/link.b"


# todo
# * sfprate => sfpr 0x01 (high) / 0x00 (low)
# * spdc    => 10mb (0x00) / 100 (0x01) / 1000 (0x02) / 10 (0x05) / 2.5 (0x03)
#   10mb (rj only) / 2.5 and 10 (sfp only)
#
# notes
# sfpo 0x18 => 24 (first sfp index ?)
# sfp 0x2 => 2 (sfp count)
# prt 0x1a => 26 (port count)


class Mikrotik_Port(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        self.parsed_data = {
            "name": []
        }

        self.parsed_data["enabled"] = utils.decode_listofflags(self._data["en"], self.port_count)
        self.parsed_data["duplex"]  = utils.decode_listofflags(self._data["dpxc"], self.port_count)
        self.parsed_data["tx_flow_control"] = utils.decode_listofflags(self._data["fctc"], self.port_count)
        self.parsed_data["rx_flow_control"] = utils.decode_listofflags(self._data["fctr"], self.port_count)
        self.parsed_data["autoneg"] = utils.decode_listofflags(self._data["an"], self.port_count)
        for i in range(0, self.port_count):
            self.parsed_data["name"].append(utils.decode_string(self._data["nm"][i]))

    def configure(self, port_id, **kwargs):
        self.parsed_data["name"][port_id-1] = kwargs.get("name", None)
        self.parsed_data["enabled"][port_id-1] = 1 if kwargs.get("enabled", 0) else 0
        self.parsed_data["autoneg"][port_id-1] = 1 if kwargs.get("autoneg", 1) else 0
        self.parsed_data["duplex"][port_id-1] = 1 if kwargs.get("duplex", 1) else 0
        self.parsed_data["tx_flow_control"][port_id-1] = 1 if kwargs.get("tx_flow_control", 0) else 0
        self.parsed_data["rx_flow_control"][port_id-1] = 1 if kwargs.get("rx_flow_control", 0) else 0

    def save(self):
        self._update_data("en", utils.encode_listofflags(self.parsed_data["enabled"], 8))
        self._update_data("dpxc", utils.encode_listofflags(self.parsed_data["duplex"], 8))
        self._update_data("fctc", utils.encode_listofflags(self.parsed_data["tx_flow_control"], 8))
        self._update_data("fctr", utils.encode_listofflags(self.parsed_data["rx_flow_control"], 8))
        self._update_data("an", utils.encode_listofflags(self.parsed_data["autoneg"], 8))
        for i in range(0, self.port_count):
            self._update_data("nm", utils.encode_string(self.parsed_data["name"][i]), i)

        return self._save(PAGE)

    def show(self):
        print("link tab")
        for i in range(0, self.port_count):
            print("* {} enabled: {}, autoneg: {}, duplex: {}, ctrl tx: {}, ctrl rx: {}".format(
                self.parsed_data["name"][i],
                self.parsed_data["enabled"][i],
                self.parsed_data["autoneg"][i],
                self.parsed_data["duplex"][i],
                self.parsed_data["tx_flow_control"][i],
                self.parsed_data["rx_flow_control"][i],
            ))
        print("")
