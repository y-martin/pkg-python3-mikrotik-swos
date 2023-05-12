#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload
# [{vid:0x64,nm:'696e7465726e6574',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0x01c20000},{vid:0x044c,nm:'70726976617465',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0xc00003},{vid:0x044d,nm:'7075626c6963',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0xc00004},{vid:0x044e,nm:'736670',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0x01c20000}]
PAGE = "/vlan.b"


class Mikrotik_Vlans(Swostab):
    def _load_tab_data(self):
        self._parsed_data = {}

        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        for i in self._data:
            self._parsed_data[int(i['vid'], 16)] = {
                "nm": utils.decode_string(i["nm"]),
                "piso": utils.decode_checkbox(i["piso"]),
                "lrn": utils.decode_checkbox(i["lrn"]),
                "mrr": utils.decode_checkbox(i["mrr"]),
                "igmp": utils.decode_checkbox(i["igmp"]),
                "mbr": utils.decode_listofflags(
                    i["mbr"], self.port_count
                )
            }

    def get(self, vlan_id):
        return self._parsed_data.get(vlan_id, None)

    def reset_member_cfg(self):
        for vlan in self._parsed_data:
            self._parsed_data[vlan]["mbr"] = [0] * self.port_count

    def add_port(self, vlan_id, port_id):
        if port_id <= 0 or port_id > self.port_count:
            return False

        _vlan_config = self.get(vlan_id)
        if _vlan_config is None:
            return False

        _vlan_config["mbr"][port_id-1] = 1
        return True

    def add(self, vlan_id, **kwargs):
        _vlan_config = self.get(vlan_id)
        if _vlan_config is None:
            _vlan_config = {
                "vid": utils.hex_str_with_pad(vlan_id, pad=4),
                "nm": str(vlan_id),
                "piso": True,
                "lrn": True,
                "mrr": False,
                "igmp": False,
                "mbr": utils.encode_listofflags([0] * self.port_count, 8)
            }
            self._parsed_data[vlan_id] = _vlan_config

        _vlan_config["piso"] = kwargs.get("port_isolation", None)
        _vlan_config["lrn"] = kwargs.get("learning", None)
        _vlan_config["mrr"] = kwargs.get("mirror", None)
        _vlan_config["igmp"] = kwargs.get("igmp_snooping", None)


    def remove(self, vlan_id):
        if self._parsed_data.pop(vlan_id, None):
            self._data_changed = True
            return True

        return False

    def save(self):
        i = 0
        while i < len(self._data):
            vlan_id = int(self._data[i]['vid'], 16)
            self._update_data(i, utils.encode_string(self._parsed_data[vlan_id]["nm"]), "nm")
            self._update_data(i, utils.encode_listofflags(self._parsed_data[vlan_id]["mbr"], 8), "mbr")
            for k in ["piso", "lrn", "mrr", "igmp"]:
                self._update_data(i, utils.encode_checkbox(self._parsed_data[vlan_id][k]), k)
            i += 1

        return self._save(PAGE)

    def show(self):
        print("vlan tab")
        for i in self._parsed_data:
            print("* vlan: {} => {}".format(i, self._parsed_data[i]))
        print("")
