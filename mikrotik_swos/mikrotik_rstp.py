#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# {ena:0x3dffff}
PAGE = "/rstp.b"


class Mikrotik_Rstp(Swostab):
    def _load_tab_data(self):
        self._page = PAGE
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        self._parsed_data = {
            "ena": utils.decode_listofflags(self._data["ena"], self.port_count)
        }

    def on_port(self, port_id, rstp_mode):
        """
        port_id             port index
        rstp_mode           true (enable) / false (disable)

        """
        
        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")

        if rstp_mode:
            self._parsed_data["ena"][port_id-1] = 1
        else:
            self._parsed_data["ena"][port_id-1] = 0

    def save(self, dry_run=False):
        self._update_data("ena", utils.encode_listofflags(self._parsed_data["ena"]))
        return self._save(dry_run)

    def show(self):
        print("rstp tab")
        print("port status {}".format(self._parsed_data["ena"]))
        print("")
