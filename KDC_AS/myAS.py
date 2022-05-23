import datetime
import json

from werkzeug.security import generate_password_hash


class myAS:

    def __init__(self):
        self.pKey = None
        self.sKey = None
        self.EKtgs = "11111111"
        self.sendmsg = None


class msgCtoA:

    def __init__(self, ID_c, ID_tgs, TS_1):
        self.id_c = ID_c
        self.id_tgs = ID_tgs
        self.ts_1 = TS_1
        self.EKc = "12345678"

class ticket_tgs:
    def __init__(self,ID_c,addr,TS_2):
        self.EKc_tgs = "as待生成"
        self.id_c = ID_c
        self.ad_c = addr
        self.id_tgs = "TGS"
        self.ts_2 = TS_2
        self.lifetime_2 = (datetime.datetime.now()+datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")

class msgAtoC:
    def __init__(self, msg_CtoA,TS_2,EKc_tgs):
        self.EKc = msg_CtoA.EKc
        self.lifetime_2 = (datetime.datetime.now()+datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        self.id_tgs = "TGS"
        self.Ekc_tgs = EKc_tgs
        self.ts_2 = TS_2


def generate_msg_to_C(src, result, target, data_msg):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': data_msg,
                      'HMAC': RSA_call(HMAC, AS_n, AS_d, 0)}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final
