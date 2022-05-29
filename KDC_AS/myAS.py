import datetime
import random
import json

from werkzeug.security import generate_password_hash

from RSA.demo_RSA import RSA_call


class myAS:

    def __init__(self):
        self.pKey = None
        self.sKey = None
        self.EKtgs = "11111111"


class msgCtoA:

    def __init__(self, ID_c, ID_tgs, TS_1):
        self.id_c = ID_c
        self.id_tgs = ID_tgs
        self.ts_1 = TS_1
        self.EKc = "12345678"


class ticket_tgs:
    def __init__(self, ID_c, addr, TS_2):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(8):
            sa.append(random.choice(seed))
        result = ''.join(sa)
        self.EKc_tgs = result
        self.id_c = ID_c
        self.ad_c = addr
        self.id_tgs = "TGS"
        self.ts_2 = TS_2
        self.lifetime_2 = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")


class msgAtoC:
    def __init__(self, TS_2, EKc_tgs):
        self.lifetime_2 = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        self.id_tgs = "TGS"
        self.Ekc_tgs = EKc_tgs
        self.ts_2 = TS_2
