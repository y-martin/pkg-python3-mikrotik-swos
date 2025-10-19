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
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    def port_lacp_mode(self, port_id, mode, group_id=None):
        """
        port_id             port index
        mode                passive / active / static
        group_id            id (static mode)

        """

        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")

        if mode not in LAG_MODE:
            raise ValueError(f"lacp mode is not in supported list {LAG_MODE}")
            return False

        _mode = LAG_MODE[mode]
        if mode == "static" and group_id:
            self._update_data("sgrp", utils.hex_str_with_pad(group_id, pad=2), port_id-1)
        
        self._update_data("mode", _mode, port_id-1)

    def save(self):
        return self._save(PAGE)

    def show(self):
        lag_mode_str = {v: k for k, v in LAG_MODE.items()}

        print("lacp tab")
        print("port status {}".format(lag_mode_str[self._data["mode"]]))
        print("")
