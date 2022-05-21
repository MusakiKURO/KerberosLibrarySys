# coding=utf-8
# @Time    : 2022/5/21 20:45
# @Author  : Nisky
# @File    : generate_msg.py
# @Software: PyCharm

import json
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from KerberosLibrarySys.RSA.demo_RSA import *

C_n = 3951270249045146953972943163348434942592764989560360906533269897277080404934010181112385167732070275357806027491762234996305583674911212807857840660608406910051955297329683233106234207322044758397760274898933802535462100186118312888112180532109135970587764285970799040141296520625252128054797411575140828014980501308928204513652682136220524500675713399801045198810206992806199335791852827154930372510398253049468928422550127057850688190116699758746503012249254107915609637655541305024737077987890330855253602741330884459042041448515721767143012038195427206379154406467638677589417430783480145088864002792702243711871
C_d = 2757273636260153892397342107350259780423194855845766289858950397671128036969148536137032681933728579320666845526660699957063082811308337204049050565811744102070678725190020954569898057638571691346945552160656416853903721986232949376871604624486124103069872348296421143823823394078988290161741459382729076515559052021058495642905456516812473319945752701566826454688598762391217175129649908066837336480981333656504068536290700516972492847182109009403521746900589327304409884664070941216444164761014904237097127620724122770288299493272459500309150609158525585771453450568861932542872871536494818060418219971795890204521


def generate_msg_to_AS(src, result, target, ID_c, ID_tgs, TS_1):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'ID_c': ID_c, 'ID_tgs': ID_tgs, 'TS_1': TS_1}}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'ID_c': ID_c, 'ID_tgs': ID_tgs, 'TS_1': TS_1},
                      'HMAC': RSA_call(HMAC, C_n, C_d, 0)}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final


def generate_msg_to_TGS(src, result, target, ID_v, TGT, ID_c, AD_c, TS_3):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'ID_v': ID_v, 'tick_tgs': TGT,
                                   'Authenticator': {'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_3}}}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'ID_v': ID_v, 'tick_tgs': TGT,
                                   'Authenticator': {'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_3}},
                      'HMAC': HMAC}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final


def generate_msg_to_S_K(src, result, target, ST, ID_c, AD_c, TS_5):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'tick_v': ST, 'Authenticator': {'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_5}}}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'tick_v': ST, 'Authenticator': {'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_5}},
                      'HMAC': HMAC}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final


def generate_msg_to_S_Search(src, result, target, select, content):
    dict_msg_orign = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'book_select': select, 'book_content': content}}
    str_msg_orign = json.dumps(dict_msg_orign)
    HMAC = generate_password_hash(str_msg_orign)
    dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                      'data_msg': {'book_select': select, 'book_content': content},
                      'HMAC': HMAC}
    str_msg_final = json.dumps(dict_msg_final)
    return str_msg_final

