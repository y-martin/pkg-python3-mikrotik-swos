#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# snmp payload
# {en:0x01,com:'7075626c6963',ci:'',loc:'626478'}
PAGE = "/snmp.b"


class Mikrotik_Snmp(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    def set(self, **kwargs):
        self._update_data("en", utils.encode_checkbox(kwargs.get("enable", None)))
        self._update_data("com", utils.encode_string(kwargs.get("community", None)))
        self._update_data("ci", utils.encode_string(kwargs.get("contact_info", None)))
        self._update_data("loc", utils.encode_string(kwargs.get("location", None)))
        return self._save(PAGE)

    def show(self):
        print("snmp tab")
        print("* enabled: {}" . format(utils.decode_checkbox(self._data["en"])))
        print("* community: {}" . format(utils.decode_string(self._data["com"])))
        print("* contact: {}" . format(utils.decode_string(self._data["ci"])))
        print("* location: {}" . format(utils.decode_string(self._data["loc"])))
        print("")
