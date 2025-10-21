#!/usr/bin/env python3


from mikrotik_swos import utils
from mikrotik_swos.swostab import Swostab


# payload poe tab
# {'poe': ['0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x01', '0x00', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02'], 'prio': ['0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07'], 'lvl': ['0x01', '0x02', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'], 'poes': ['0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x03', '0x01', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02', '0x02'], 'std': ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'], 'curr': ['0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0074', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000'], 'volt': ['0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x020e', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000'], 'pwr': ['0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x003d', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000'], 'lldp': '0x00000040', 'ldpw': ['0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000', '0x0000']}

PAGE = "/poe.b"


# poe
POE_OUT_MODE = {
    "off":  "0x00",    
    "on":   "0x01",
    "auto": "0x02"
}

# lvl
VOLTAGE_LEVEL = {
    "auto": "0x00",
    "low":  "0x01",
    "high": "0x02"
}

# poes
POE_STATUS = {
    "short circuit":    "0x00",  # to be confirmed
    "disabled":         "0x01",
    "waiting for load": "0x02",
    "powered on":       "0x03"
}

POE_MIN_PRIORITY = 1
POE_MAX_PRIORITY = 8


class Mikrotik_Poe(Swostab):
    def _load_tab_data(self):
        self._page = PAGE
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        self.parsed_data = {
            "lldp": utils.decode_listofflags(self._data["lldp"], self.port_count)
        }

    def configure_port(self, port_id, **kwargs):
        """
        port_id             port index 1..port_count
        priority            priority 1..8
        lldp_enabled        1 (enable) / 0 (disable)
        poe_output          on / off / auto
        voltage_level       auto / low / high

        """
        if port_id < 1 or port_id > self.port_count:
            raise ValueError(f"port_id is outside 1..{self.port_count}")

        priority = kwargs.get("priority", None)
        if priority is not None:
            if priority < POE_MIN_PRIORITY or priority > POE_MAX_PRIORITY:
                raise ValueError(f"priority is outside {POE_MIN_PRIORITY}..{POE_MAX_PRIORITY} range")

            self._update_data("prio", utils.hex_str_with_pad(priority-1, pad=2), port_id-1)
            
        self.parsed_data["lldp"][port_id-1] = 1 if kwargs.get("lldp_enabled", 0) else 0
        self._update_data("lldp", utils.encode_listofflags(self.parsed_data["lldp"], 8))

        self._update_data("poe", POE_OUT_MODE.get(kwargs.get("poe_output"), "0x02"), port_id-1)
        self._update_data("lvl", VOLTAGE_LEVEL.get(kwargs.get("voltage_level"), "0x00"), port_id-1)

    def show(self):
        poe_out_mode_str = {v: k for k, v in POE_OUT_MODE.items()}
        voltage_level_str = {v: k for k, v in VOLTAGE_LEVEL.items()}
        poe_status_str = {v: k for k, v in POE_STATUS.items()}

        print("poe tab")

        for i in range(0, self.port_count):
            # indexed fpX
            print(f"port {i+1}")
            print(f"  poe out: {poe_out_mode_str.get(self._data['poe'][i], 'unknown')}")
            print(f"  poe priority: {int(self._data['prio'][i], 16)+1}")
            print(f"  voltage level: {voltage_level_str.get(self._data['lvl'][i], 'unknown')}")
            print(f"  lldp: {self.parsed_data['lldp'][i]}")
            print(f"  poe status: {poe_status_str.get(self._data['poes'][i], 'unknown')}")
            print(f"  poe current: {int(self._data['curr'][i], 16)} mA")
            print(f"  poe voltage: {round(int(self._data['volt'][i], 16)*0.1, 2)} V")
            print(f"  poe power: {round(int(self._data['pwr'][i], 16)*0.1, 2)} W")
        print("")
