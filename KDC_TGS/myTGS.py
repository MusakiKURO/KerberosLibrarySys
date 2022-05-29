import datetime
import json
from random import random

from werkzeug.security import generate_password_hash

from RSA.demo_RSA import RSA_call


class myTGS:

    def __init__(self):
        self.pKey = None
        self.sKey = None
        self.EKtgs = "11111111"


class msgCtoT:

    def __init__(self, ID_v, ticket_tgs):
        self.id_v = ID_v
        self.ticket_tgs = ticket_tgs


class ticket_tgs:
    def __init__(self, EKc_tgs, ID_c, AD_c, ID_tgs, TS_2, Lifetime_2):
        self.EKc_tgs = EKc_tgs
        self.id_c = ID_c
        self.ad_c = AD_c
        self.id_tgs = ID_tgs
        self.ts_2 = TS_2
        self.lifetime_2 = Lifetime_2


class ticket_v:
    def __init__(self, id_c, ad_c, id_v, ts_4):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(8):
            sa.append(random.choice(seed))
        result = ''.join(sa)
        self.EKc_v = result
        self.id_c = id_c
        self.ad_c = ad_c
        self.id_v = id_v
        self.ts_4 = ts_4
        self.lifetime_4 = (datetime.datetime.now()+datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
