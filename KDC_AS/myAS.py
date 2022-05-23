import datetime


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
    def __init__(self, msg_CtoA, TS_2,EKc_tgs):
        self.EKc = msg_CtoA.EKc
        self.ts_2 = TS_2
        self.id_tgs = "TGS"
        self.Ekc_tgs = EKc_tgs
