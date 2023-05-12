#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# {ena:0x3dffff}
PAGE = "/rstp.b"


class Mikrotik_Rstp(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        self._parsed_data["ena"] = utils.decode_listofflags(self._data["ena"], self.port_count)

    def on_port(self, port_id, rstp_mode):
        if port_id > 0 and port_id <= self.port_count:
            self._parsed_data["ena"][port_id-1] = rstp_mode
            return True

        return False

    def save(self):
        self._update_data("ena", utils.encode_listofflags(self_parsed_data["ena"], 8))
        return self._save(PAGE)

    def show(self):
        print("rstp tab")
        print("port status {}".format(utils.decode_listofflags(self._data["ena"], self.port_count)))
        print("")
