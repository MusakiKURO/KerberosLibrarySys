import datetime
import json

from werkzeug.security import generate_password_hash

from RSA.demo_RSA import RSA_call


class myTGS:

    def __init__(self):
        self.pKey = None
        self.sKey = None
        self.EKtgs = "11111111"