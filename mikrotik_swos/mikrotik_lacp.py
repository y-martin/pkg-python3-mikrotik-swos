#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# {mode:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00],sgrp:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00]}
PAGE = "/lacp.b"


LAG_MODE = {
    "passive": "0x00",
    "active": "0x01",
    "static": "0x02"
}


class Mikrotik_Lacp(Swostab):
    def _load_tab_data(self):
        self._page = PAGE
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    def port_lacp_mode(self, port_id, mode, group_id=None):
        """
        port_id             port index
        mode                passive / active / static
        group_id            id 1..15 (static mode only)

        """

        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")

        if mode not in LAG_MODE:
            raise ValueError(f"lacp mode is not in supported list {LAG_MODE}")

        if group_id is not None and not isinstance(group_id, int):
            raise ValueError(f"group id is outside 0..15")

        if mode == "static" and isinstance(group_id, int):
            if group_id < 0 or group_id > 15:
                raise ValueError(f"group id is outside 0..15")
            self._update_data("sgrp", utils.hex_str_with_pad(group_id, pad=2), port_id-1)

        self._update_data("mode", LAG_MODE[mode], port_id-1)

    def show(self):
        lag_mode_str = {v: k for k, v in LAG_MODE.items()}

        print("lacp tab")
        for i in range(0, self.port_count):
            if lag_mode_str[self._data["mode"][i]] == "static":
                print(f"* port {i+1} status {lag_mode_str[self._data['mode'][i]]} group {int(self._data['sgrp'][i], 16)}")
            else:
                print(f"* port {i+1} status {lag_mode_str[self._data['mode'][i]]}")
        print("")
