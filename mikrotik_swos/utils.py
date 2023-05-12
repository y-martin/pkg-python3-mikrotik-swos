#!/usr/bin/env python3


import json
import re
import socket
import struct


def mikrotik_to_json(broken_json):
    result = re.sub(r'([{,])([a-zA-Z][a-zA-Z0-9]+)', '\\1"\\2"', broken_json)
    result = re.sub(r'\'', '"', result)
    result = re.sub(r'(0x[0-9a-zA-Z]+)', '"\\1"', result)
    return json.loads(result)

def json_to_mikrotik(data):
    result = re.sub(r'"(0x[0-9a-zA-Z]+)"', '\\1', json.dumps(data))
    result = re.sub(r'"([a-zA-Z][a-zA-Z0-9]+)":', '\\1:', result)
    result = re.sub(r'"', '\'', result)
    return result.replace(" ", "")

# 53465031 -> SFP1
def decode_string(s):
    return bytes.fromhex(s).decode("ascii")

# SFP1 -> 53465031
def encode_string(s):
    if isinstance(s, str):
        return s.encode("ascii").hex()

    return None

# 0x1c20005 -> [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0]
def decode_listofflags(s, zfill=0):
    flags = []

    if len(s) == 0:
        return flags

    # list is reversed (example port1 is last item)
    flags_str = bin(int(s, 16))[2:]
    if zfill > 0:
        flags_str = flags_str.zfill(zfill)

    flags_list = list(flags_str)
    i = len(flags_list)
    while i:
        flags.append(int(flags_list[i-1]))
        i -= 1
    return flags

# [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0] --> 0x1c20005
# with hex_len_str=8 => 0xc26005 becomes 0x00c26005
def encode_listofflags(flags, hex_len_str=0):
    if flags is None or len(flags) == 0:
        return None

    # list need to be reversed
    flags_str = ""
    i = len(flags)
    while i:
        flags_str += str(flags[i-1])
        i -= 1

    return hex_str_with_pad(int(flags_str, 2), hex_len_str)

# with pad=8 => 0xc26005 becomes 0x00c26005
def hex_str_with_pad(s, pad=0):
    if s is None:
        return None

    if pad == 0:
        return hex(s)
    else:
        return '0x{0:0{1}x}'.format(s,pad)

# 10.31.0.250 => 0xfa001f0a
def encode_ipv4(s):
    if isinstance(s, str):
        return hex_str_with_pad(struct.unpack("I", socket.inet_aton(s))[0], 8)

    return None

# 0xfa001f0a => 10.31.0.250
def decode_ipv4(s):
    if s == "0x00000000":
        return ""

    return socket.inet_ntoa(struct.pack("<L", int(s, 16)))

# true => 0x01 / false => 0x00 / None => None
def encode_checkbox(s):
    if s is None:
        return None

    return "0x01" if s else "0x00"

# 0x01 => true
def decode_checkbox(s):
    return s == "0x01"

# [1, 3, 4] --> [1, 0, 1, 1]
def ports_to_flag_list(ports, fill=0):
    if not isinstance(ports, list):
        return None

    if not fill and len(ports):
        fill = max(ports)

    flag_list = [0] * fill
    for i in ports:
        flag_list[i-1] = 1

    return flag_list
