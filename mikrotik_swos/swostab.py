#!/usr/bin/env python3


import logging
import requests
from mikrotik_swos import utils


class Swostab:
    def _get(self, page):
        ret = requests.get(self._url + page, auth=self._auth)
        logging.debug(f"--- got headers: {ret.headers}")
        logging.debug(f"--- got data: {ret.text}")
        return ret

    def _post(self, page, data):
        logging.debug(f"--- posted: {data}")
        ret = requests.post(self._url + page, auth=self._auth, data=data)
        logging.debug(f"--- got headers: {ret.headers}")
        logging.debug(f"--- got data: {ret.text}")
        return ret

    def _update_data(self, field, value = None, field_index = None):
        if value is None:
            return

        if field_index is not None:
            old_value = self._data[field][field_index]
            if value.startswith("0x"):
                value = utils.hex_str_with_pad(value, utils.hex_value_len(old_value))
            if value != old_value:
                logging.debug(f"update data ({field}/{field_index}): {old_value} -> {value}")
                self._data[field][field_index] = value
                self._data_changed = True
            return

        old_value = self._data[field]
        if value.startswith("0x"):
            value = utils.hex_str_with_pad(value, utils.hex_value_len(old_value))
        if value != old_value:
            logging.debug(f"update data ({field}): {old_value} -> {value}")
            self._data[field] = value
            self._data_changed = True

    def __init__(self, url, login, password):
        if 'http://' not in url:
            self._url = "http://%s" % url
        else:
            self._url  = url
        self._auth = requests.auth.HTTPDigestAuth(login, password)

        resp = self._get("/link.b")
        assert(resp.status_code == 200)

        # required to decode some list of boxes
        _link = utils.mikrotik_to_json(resp.text)
        self.port_count = int(_link["prt"], 16)
        self.sfp_count = int(_link["sfp"], 16)
        self.sfp_first_port_id = int(_link["sfpo"], 16) + 1

        # some feature appears in 2.16
        resp = self._get("/sys.b")
        assert(resp.status_code == 200)

        # required to decode some list of boxes
        _sys = utils.mikrotik_to_json(resp.text)
        self.version = float(utils.decode_string(_sys["ver"]))

        self._load_tab_data()
        self._data_changed = False

    def show(self):
        raise Exception("not implemented")

    def _load_tab_data(self):
        raise Exception("not implemented")

    def save(self):
        return self._save()

    def _save(self):
        if self._data_changed:
            return self._post(self._page, utils.json_to_mikrotik(self._data)).ok

        return False
