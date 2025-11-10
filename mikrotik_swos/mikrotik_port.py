#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# {en:0x03c20007,nm:['6d657a7a5f6c6170746f70','6d657a7a5f67616d65','627572656175','506f727434','506f727435','506f727436','506f727437','506f727438','506f727439','506f72743130','506f72743131','506f72743132','506f72743133','506f72743134','506f72743135','506f72743136','506f72743137','6e6574','506f72743139','506f72743230','506f72743231','506f72743232','6865795f31','6865795f32','53465031','53465032'],an:0x03ffffff,spdc:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01],dpxc:0x03ffffff,fctc:0x03ffffff,fctr:0x03ffffff}
PAGE = "/link.b"


# notes
# sfpo 0x18 => 24 (first sfp index ?)
# sfp 0x2 => 2 (sfp count)
# prt 0x1a => 26 (port count)


PORT_SPEED_MB = {
    "10": "0x00",
    "100": "0x01",
    "1000": "0x02",
    "2500": "0x05",
    "10000": "0x03"
}

COMBO_MODE = {
    "auto": "0x00",
    "copper": "0x01",
    "sfp": "0x02"
}

PORT_SFP_RATE = {
    "low": "0x00",
    "high": "0x01"
}

PORT_NAME_LENGTH_MAX = 16

class Mikrotik_Port(Swostab):
    def _load_tab_data(self):
        self._page = PAGE
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        self.parsed_data = {
            "name": [],
            "speed": [],
        }

        self.parsed_data["enabled"] = utils.decode_listofflags(self._data["en"], self.port_count)
        self.parsed_data["duplex"]  = utils.decode_listofflags(self._data["dpxc"], self.port_count)
        self.parsed_data["tx_flow_control"] = utils.decode_listofflags(self._data["fctc"], self.port_count)
        self.parsed_data["rx_flow_control"] = utils.decode_listofflags(self._data["fctr"], self.port_count)
        self.parsed_data["autoneg"] = utils.decode_listofflags(self._data["an"], self.port_count)
        self.parsed_data["speed"] = self._data["spdc"].copy()
        for i in range(0, self.port_count):
            self.parsed_data["name"].append(utils.decode_string(self._data["nm"][i]))

        if self.version >= 2.16:
            self.parsed_data["sfp_rate"] = self._data["sfpr"].copy()

        self.parsed_data["combo_mode"] = self._data["cm"].copy()
        self.parsed_data["combo_port"] = utils.decode_listofflags(self._data["comb"], self.port_count)

    def _is_sfp_port(self, port_id):
        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")
        return port_id >= self.sfp_first_port_id and port_id < (self.sfp_first_port_id + self.sfp_count)

    def _is_combo_port(self, port_id):
        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")
        return 1 == self.parsed_data["combo_port"][port_id-1]

    def configure(self, port_id, **kwargs):
        """
        port_id             port index
        name                port name
        enabled             1 (enable) / 0 (disable)
        autoneg             1 (enable) / 0 (disable)
        duplex              1 (enable) / 0 (disable)
        tx_flow_control     1 (enable) / 0 (disable)
        rx_flow_control     1 (enable) / 0 (disable)
        speed               10 / 100 / 1000 / 2500 / 10000
        sfp_rate            low / high
        combo_mode          auto / copper / sfp

        """
        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")

        port_name = kwargs.get("name")
        if port_name is not None:
            if len(port_name) <= PORT_NAME_LENGTH_MAX:
                self.parsed_data["name"][port_id-1] = port_name
            else:
                raise ValueError(f"port name length is greater than {PORT_NAME_LENGTH_MAX}")

        self.parsed_data["enabled"][port_id-1] = 1 if kwargs.get("enabled", 0) else 0
        self.parsed_data["autoneg"][port_id-1] = 1 if kwargs.get("autoneg", 1) else 0
        self.parsed_data["duplex"][port_id-1] = 1 if kwargs.get("duplex", 1) else 0
        self.parsed_data["tx_flow_control"][port_id-1] = 1 if kwargs.get("tx_flow_control", 0) else 0
        self.parsed_data["rx_flow_control"][port_id-1] = 1 if kwargs.get("rx_flow_control", 0) else 0
        if kwargs.get("autoneg", 1) == 0 and kwargs.get("speed"):
            self.parsed_data["speed"][port_id-1] = PORT_SPEED_MB.get(str(kwargs.get("speed")), "0x02")

        if self.version >= 2.16:
            if kwargs.get("sfp_rate"):
                if not self._is_sfp_port(port_id):
                    raise ValueError(f"can't set sfp_rate on non-sfp port")
                self.parsed_data["sfp_rate"][port_id-1] = PORT_SFP_RATE.get(kwargs.get("sfp_rate"), "0x00")

            if kwargs.get("combo_mode"):
                if not self._is_combo_port(port_id):
                    raise ValueError(f"can't set combo_mode on non-combo port")
                self.parsed_data["combo_mode"][port_id-1] = COMBO_MODE.get(kwargs.get("combo_mode"), "0x00")

    def save(self, dry_run=False):
        self._update_data("en", utils.encode_listofflags(self.parsed_data["enabled"]))
        self._update_data("dpxc", utils.encode_listofflags(self.parsed_data["duplex"]))
        self._update_data("fctc", utils.encode_listofflags(self.parsed_data["tx_flow_control"]))
        self._update_data("fctr", utils.encode_listofflags(self.parsed_data["rx_flow_control"]))
        self._update_data("an", utils.encode_listofflags(self.parsed_data["autoneg"]))
        for i in range(0, self.port_count):
            self._update_data("nm", utils.encode_string(self.parsed_data["name"][i]), i)
            self._update_data("spdc", self.parsed_data["speed"][i], i)

        if self.version >= 2.16:
            for i in range(0, self.port_count):
                self._update_data("sfpr", self.parsed_data["sfp_rate"][i], i)
                self._update_data("cm", self.parsed_data["combo_mode"][i], i)

        return self._save(dry_run)

    def show(self):
        port_speed_mb_str = {v: k for k, v in PORT_SPEED_MB.items()}
        combo_mode_str = {v: k for k, v in COMBO_MODE.items()}
        sfp_rate_str = {v: k for k, v in PORT_SFP_RATE.items()}

        print("link tab")
        for i in range(0, self.port_count):
            properties = [
                f"enabled: {self.parsed_data['enabled'][i]}",
                f"full duplex: {self.parsed_data['duplex'][i]}",
                f"flow ctrl tx: {self.parsed_data['tx_flow_control'][i]}",
                f"flow ctrl tx: {self.parsed_data['rx_flow_control'][i]}",
                f"autoneg: {self.parsed_data['autoneg'][i]}"
            ]

            if self.parsed_data['autoneg'][i] == 0:
                properties.append(f"speed: {port_speed_mb_str[self.parsed_data['speed'][i]]}mb/s")

            if self.version >= 2.16:
                if self._is_combo_port(i+1):
                    properties.append(f"combo mode: {combo_mode_str[self.parsed_data['combo_mode'][i]]}")
                if self._is_sfp_port(i+1):
                    properties.append(f"sfp rate: {sfp_rate_str[self.parsed_data['sfp_rate'][i]]}")

            print(f"* {self.parsed_data['name'][i]} {', '.join(properties)}")

        print("")
