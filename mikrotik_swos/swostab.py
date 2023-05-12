#!/usr/bin/env python3


import requests
from mikrotik_swos import utils


class Swostab:
    def _get(self, page):
        return requests.get(self._url + page, auth=self._auth)

    def _post(self, page, data):
        return requests.post(self._url + page, auth=self._auth, data=data)
    def _update_data(self, field, value = None, field_index = None):
        if value is None:
            return

        if field_index is not None:
            if value != self._data[field][field_index]:
                self._data[field][field_index] = value
                self._data_changed = True
            return

        if value != self._data[field]:
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
        self.port_count = len(_link["nm"])

        self._load_tab_data()
        self._data_changed = False

    def show(self):
        raise Exception("not implemented")

    def _load_tab_data(self):
        raise Exception("not implemented")

    def _save(self, page):
        if self._data_changed:
            return self._post(page, utils.json_to_mikrotik(self._data)).ok

        return False
