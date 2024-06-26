from mikrotik_swos import utils


# test_mikrotik_to_json

def test_mikrotik_to_json_port():
    port_panel = "{comb:0x00000000,qsfp:0x00000000,en:0x01c20007,blkp:0x00000000,an:0x03ffffff,dpxc:0x03ffffff,fctc:0x03ffffff,fctr:0x03ffffff,lnk:0x00c20003,dpx:0x00c20003,tfct:0x00c00001,rfct:0x00c00001,paus:0x00000000,spd:[0x02,0x00,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x02,0x07,0x07,0x07,0x07,0x02,0x02,0x07,0x07],spdc:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x02,0x02],cm:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],qtyp:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],prt:0x1a,sfp:0x02,sfpo:0x18,nm:['6d657a7a5f6c6170746f70','6d657a7a5f67616d65','627572656175','506f727434','506f727435','506f727436','506f727437','506f727438','506f727439','506f72743130','506f72743131','506f72743132','506f72743133','506f72743134','506f72743135','506f72743136','506f72743137','6e6574','506f72743139','506f72743230','506f72743231','506f72743232','6865795f31','6865795f32','53465031','53465032'],hop:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],hops:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],len:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],flt:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],pair:[0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff]}"
    context = utils.mikrotik_to_json(port_panel)
    assert(context["comb"] == "0x00000000")
    assert(len(context["nm"]) == 26)

def test_mikrotik_to_json_snmp():
    snmp_panel = "{en:0x01,com:'7075626c6963',ci:'',loc:'626478'}"
    context = utils.mikrotik_to_json(snmp_panel)
    assert(context["com"] == '7075626c6963')


# test_json_to_mikrotik

def test_json_to_mikrotik_port():
    panel_data = "{comb:0x00000000,qsfp:0x00000000,en:0x03c20007,blkp:0x00000000,an:0x03ffffff,dpxc:0x03ffffff,fctc:0x03ffffff,fctr:0x03ffffff,lnk:0x00c20007,dpx:0x00c20007,tfct:0x00c00005,rfct:0x00c00005,paus:0x00000000,spd:[0x02,0x00,0x02,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x02,0x07,0x07,0x07,0x07,0x02,0x02,0x07,0x07],spdc:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01],cm:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],qtyp:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],prt:0x1a,sfp:0x02,sfpo:0x18,nm:['506f727431','506f727432','506f727433','506f727434','506f727435','506f727436','506f727437','506f727438','506f727439','506f72743130','506f72743131','506f72743132','506f72743133','506f72743134','506f72743135','506f72743136','506f72743137','506f72743138','506f72743139','506f72743230','506f72743231','506f72743232','506f72743233','506f72743234','53465031','53465032'],hop:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],hops:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],len:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],flt:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],pair:[0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff]}"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_data)) == panel_data)

def test_mikrotik_to_json_snmp():
    panel_datapanel = "{en:0x01,com:'7075626c6963',ci:'',loc:'626478'}"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_datapanel)) == panel_datapanel)

def test_mikrotik_to_json_system():
    panel_data = "{upt:0x0915b7ea,cip:0xfa001f0a,mac:'2cc81b1dc201',sid:'443237373045413335393535',id:'4d696b726f54696b',ver:'322e3133',brd:'4353533332362d3234472d32532b',wdt:0x01,dsc:0x00,bld:0x6086781d,ivl:0x00,alla:0x00000000,allm:0x00,avln:0x044c,allp:0x00c00003,temp:0x0000003b,btmp:0x00000000,fan1:0x00000000,fan2:0x00000000,fan3:0x00000000,fan4:0x00000000,p1v:0x00000000,p2v:0x00000000,p1c:0x00000000,p2c:0x00000000,p1s:0x00,p2s:0x00,prio:0x8000,rpr:0x8000,cost:0x00,rmac:'2cc81b1dc201',poe:0x00,poes:0x00,igmp:0x01,igfl:0x01020000,ip:0xfa001f0a,dtrp:0x01c20000,ainf:0x01,iptp:0x01,upgr:0x00,npoe:0x00}"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_data)) == panel_data)

def test_mikrotik_to_json_vlans():
    panel_data = "[{nm:'696e7465726e6574',mbr:0x01c20000,vid:0x0064,piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00},{nm:'70726976617465',mbr:0x00c00003,vid:0x044c,piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00},{nm:'7075626c6963',mbr:0x00c00004,vid:0x044d,piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00},{nm:'736670',mbr:0x01c20000,vid:0x044e,piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00}]"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_data)) == panel_data)

def test_mikrotik_to_json_vlan():
    panel_data = "{fp1:0x00fdfffe,fp2:0x00fdfffd,fp3:0x00fdfffb,fp4:0x00fdfff7,fp5:0x00fdffef,fp6:0x00fdffdf,fp7:0x00fdffbf,fp8:0x00fdff7f,fp9:0x00fdfeff,fp10:0x00fdfdff,fp11:0x00fdfbff,fp12:0x00fdf7ff,fp13:0x00fdefff,fp14:0x00fddfff,fp15:0x00fdbfff,fp16:0x00fd7fff,fp17:0x00fcffff,fp18:0x00c00000,fp19:0x00f9ffff,fp20:0x00f5ffff,fp21:0x00edffff,fp22:0x00ddffff,fp23:0x01bfffff,fp24:0x017fffff,fp25:0x00c00000,fp26:0x00000000,lck:0x00000000,lckf:0x00000000,imr:0x00000000,omr:0x00000000,mrto:0x00400000,vlan:[0x03,0x03,0x03,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x02,0x01,0x01,0x01,0x02,0x02,0x02,0x02,0x01],vlni:[0x02,0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x00,0x00],dvid:[0x044c,0x044c,0x044d,0x0000,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x044e,0x0001,0x0001,0x0001,0x044c,0x0001,0x0001,0x044e,0x0001],fvid:0x00000007,srt:[0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64,0x64],suni:0x00000000,fmc:0x03ffffff,ir:[0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000]}"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_data)) == panel_data)

def test_mikrotik_to_json_lacp():
    panel_data = "{mode:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00],grp:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00],sgrp:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x00,0x00],mac:['000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','000000000000','fa66bc79869f','fa66bc79869f','000000000000','000000000000']}"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_data)) == panel_data)

def test_mikrotik_to_json_rstp():
    panel_data = "{rpc:[0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000],cst:[0x00000004,0x00000064,0x00000004,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000004,0x00000000,0x00000000,0x00000000,0x00000000,0x00000004,0x00000004,0x00000000,0x00000000],ena:0x003dffff,rstp:0x03ffffff,p2p:0x03ffffff,edge:0x03c20007,lrn:0x03c20007,fwd:0x03c20007,role:[0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00]}"
    assert(utils.json_to_mikrotik(utils.mikrotik_to_json(panel_data)) == panel_data)


# test_decode_string

def test_decode_string():
    assert(utils.decode_string("53465031") == "SFP1")


# test_encode_string

def test_encode_string():
    assert(utils.encode_string("SFP1") == "53465031")
    assert(utils.decode_string(utils.encode_string("SFP1")) == "SFP1")


# test_decode_listofflags

def test_decode_listofflags():
    flags = utils.decode_listofflags("0x03c20007", zfill=26)

    assert(len(flags) == 26)
    assert(flags == [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1])

    flags = utils.decode_listofflags("0x00c26005", zfill=26)

    assert(len(flags) == 26)
    assert(flags == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0])


def test_encode_listofflags():
    flags = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1]
    assert(utils.encode_listofflags(flags, 8) == "0x03c20007")

    flags = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0]
    assert(utils.encode_listofflags(flags, 8) == "0x00c26005")


# test_encode_ipv4

def test_encode_ipv4():
    assert(utils.encode_ipv4("10.31.0.250") == "0xfa001f0a")


# test_decode_ipv4

def test_decode_ipv4():
    assert(utils.decode_ipv4("0xfa001f0a") == "10.31.0.250")


# test_decode_checkbox

def test_decode_checkbox():
    assert(utils.decode_checkbox("0x01") == True)
    assert(utils.decode_checkbox("0x00") == False)

def test_encode_checkbox():
    assert(utils.encode_checkbox(True) == "0x01")
    assert(utils.encode_checkbox(False) == "0x00")


# test_ports_to_flag_list
def test_ports_to_flag_list():
    assert(utils.ports_to_flag_list(None) == None)
    assert(utils.ports_to_flag_list([]) == [])
    assert(utils.ports_to_flag_list([], 2) == [0, 0])
    assert(utils.ports_to_flag_list([4]) == [0, 0, 0, 1])
    assert(utils.ports_to_flag_list([2], 4) == [0, 1, 0, 0])
