
class myAS:

    def __init__(self):
        self.pKey = None
        self.sKey = None
        self.EKtgs = None
        self.sendmsg = None


class msgCtoA:

    def __init__(self,ID_c,ID_tgs,TS_1):
        self.id_c = ID_c
        self.id_tgs = ID_tgs
        self.ts_1 = TS_1
        self.EKc = "12345678"
