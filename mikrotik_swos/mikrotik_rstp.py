#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# {ena:0x3dffff}
PAGE = "/rstp.b"


class Mikrotik_Rstp(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        self._parsed_data = {
            "ena": utils.decode_listofflags(self._data["ena"], self.port_count)
        }

    def on_port(self, port_id, rstp_mode):
        if port_id < 1 or port_id > self.port_count:
            return False

        if rstp_mode:
            self._parsed_data["ena"][port_id-1] = 1
        else:
            self._parsed_data["ena"][port_id-1] = 0

        return True


    def save(self):
        self._update_data("ena", utils.encode_listofflags(self._parsed_data["ena"], 8))
        return self._save(PAGE)

    def show(self):
        print("rstp tab")
        print("port status {}".format(self._parsed_data["ena"]))
        print("")
