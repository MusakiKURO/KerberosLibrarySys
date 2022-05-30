# coding=utf-8
# @Time    : 2022/5/25 20:44
# @Author  : Nisky
# @File    : demo_manager_logic.py
# @Software: PyCharm
# coding=utf-8
# @Time    : 2022/5/19 15:24
# @Author  : Nisky
# @File    : demo_reader_logic.py
# @Software: PyCharm

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from Client import demo_manager_MainWindow
from Client import demo_manager_Dialog
from DES.demo_DES import DES_call
from RSA.demo_RSA import RSA_call
from werkzeug.security import generate_password_hash, check_password_hash
import json
import socket
import sys
import time
from datetime import datetime, timedelta

# 要连接的目标IP和Port
# AS
AS_IP = '127.0.0.1'
AS_Port = 7788
# TGS
TGS_IP = ''
TGS_Port = None
# Server
S_IP = ''
S_Port = None

# 主体的密钥部分
# AS
AS_n = 3154524864060864374678451683785718402763405879146890491724664939645203946720547999949914217988518171750442418164607972417886195034362711226485418090182244227302447541186973733483464033984189667761796827741079639931123803417438545627319420211895141018230052852282054657816721996634088748902963118173646405921325251595289523097960744361920052328324763552082601036203542971235280005631770562170683186175141376336290714492185920922938387369254486603274876452521823106930391534430591715961317922064788106395009561894542301754552240585726394934679113208017542471920011881673470137586116357477440647703346142468530016520721
AS_e = 65537
AS_d = 46208155232897901943807522718987589707384678028915190992197969727930722932873431495978113878709392326173378724049371401211083010100984219256694712400246493709055184697796584893176762327003403894766695982901818123104183152734196008395664180591411498504674469966442963081985033138055223750657561277548568742607930841370467181838938224220146263084906859210409331342014259529147676447743956246406207635534153009989102097371654411928251651146150897767918673659121141136736827874109137846992571374515725993944656407671110428274379442278052200277489961831219425908455297367981451238069320319055904678698062056760825644033
# TGS
TGS_n = 14220740661786976075675484623124052254340247802148417953610565874929344370990160272496763287697887046488412860516140652697481778540855238640459761025038289099157228983802767721981144334696822749252844010939010650982385066579660472052903373434694773981620284873744629391760163314379404877893893830380183489587092045771675932640410147971024868813649655435174684648383133844519036758245419838996354750519894444497111923680728163499972430979364192040736679729753637059055728567923233332769769871876953627404607873684684160726342106273987685360916603193012258592402006915529292108505528446791863340231851499687122542135669
TGS_e = 65537
TGS_d = 11088085323058951088194718468065963809707289968869251833765657814805216860057634464876094481000992234547780599850081440298477484221702285648221520490401705494101567070087453356016242359323857400961599233394623560205683459758924731402160037574391610089885050537076011442680384292304920720514792784723551220194504377711863943736386695266582777078417547844050682645898493076915367194528605178758376493593347535909210633380372427613442488820455934576107941882610731347354040440402701256658054138541204052213518159717834596831041571266118419547907155814200537861651127258322924866528549026560868077022568496698160229001473
# S
S_n = 10469390129546136402029942747457300548433313561152500694655265739940475404319462139530628254855322586969734523342743903668412559804045845034210748615835404649037119900853265926666451144690640278649024315138788684707831566351503299322478262056212399670974114581850558320339645904277358701922873391829160151236405533264476749760758974104883363191923240109341780901794063881916334145879532060236519390370906919172355572965775460432228690239610801536843235695767284700782343713226170627931582080505723902106175293364974962491182627509560208769591792202469015835052126845105188154599166838191586917087104257804552326005823
S_e = 65537
S_d = 8110714186754298143092669075085860864016604301796462536720282468655230133025737091234707993278826287221376645546146352091988380401468111815874210426525400382088173880496849377126036552149674050194062324003640372613730019482102102830475400477867707647507480439289508934499359168896502067748418875596229903696601538947599762970083498153007126984514457653542261324691019431373092778414249493081800991492478535451747689826738343974509191893347816832399493117974542984766167012840616050188269725303380603488917126926095089931521535057761266939722944819520741894548836638416431206454098874309067605170447054752532589197921
# C
# C_n_1 注册测试
C_n_1 = 3951270249045146953972943163348434942592764989560360906533269897277080404934010181112385167732070275357806027491762234996305583674911212807857840660608406910051955297329683233106234207322044758397760274898933802535462100186118312888112180532109135970587764285970799040141296520625252128054797411575140828014980501308928204513652682136220524500675713399801045198810206992806199335791852827154930372510398253049468928422550127057850688190116699758746503012249254107915609637655541305024737077987890330855253602741330884459042041448515721767143012038195427206379154406467638677589417430783480145088864002792702243711871
C_e_1 = 65537
C_d_1 = 2757273636260153892397342107350259780423194855845766289858950397671128036969148536137032681933728579320666845526660699957063082811308337204049050565811744102070678725190020954569898057638571691346945552160656416853903721986232949376871604624486124103069872348296421143823823394078988290161741459382729076515559052021058495642905456516812473319945752701566826454688598762391217175129649908066837336480981333656504068536290700516972492847182109009403521746900589327304409884664070941216444164761014904237097127620724122770288299493272459500309150609158525585771453450568861932542872871536494818060418219971795890204521

C_n_2 = 2440377791864065274813867079683927118448249889237816829169332581163550200188754797695239559187402583824434016024383686718297339595321863528950898122117152257275170703752818364764988933320158047486977517208831918337392866844036736478998044963921785922013825256822302265204998231469222373247560352424688661160793664441560098580623986633890529752536456629687210963738777154840220133258368897771955948362510942683542834447030780606971377840741148347035961537716669133482168102975994612355608633388001131737009273091650029420343335464720087854056903286322179538661549404577746037343631153361099095498771745166881003667029
C_e_2 = 65537
C_d_2 = 2208430750261287262441991985624827952773682109814554228975613420261040866576051231238983593638501494445268056553918362022808163582699072007797425360125182203556400569116257252811113777825532653010630065316102406468927417287732590248202024058474957344138363799557762832366114334070473785992131305699123168837724288522599915633752416259160413149871833133277662366347388925200457243671530913111321014521051777948182370677613471220975732470408520310076720596981149789004587491601175305299766492704513532773199426769935506009334136239018308615860447970196385434673787095433505218964380490613200473196668209563753786617473
C_n_3 = 2227759266440993576821443425907433253575944905979418392944755142859200449887391797382987228341852410464110067700354735935584533383575049395899510837595966740795349469627399769813392924130137427549420210642209831971749335040086682409018633007396040256637118364013243311115981566433674861198761119177453991822215629642409296240314473143563319657581944972614606011350430167955930434657700226142447639934083796471058014262323429703922649276782856434725260008391650022129450773192211070891973588757030144986954070288928438777172490961055882300095862833574639894246041670433652610085390923063314646680984784651447153181167
C_e_3 = 65537
C_d_3 = 1610661417546936824244784684220698381894029288493870358925512808552382545997135748285671969124647035491721124522726222635088605601628645887451462868575151320309230570812748268811022734090030085746588611637087881171207085191638727323291116282244328783438921211560485036095771160753876679557820744159563338183105940918791467956039589787866524525570914255656843711295607537869025734402678460848028218928734089070332444358303058651734052706943050466441032957794017845675009535131138932138376182123648371021198145942474986776781392161018642935551980041518391024427744833314056764311534237436781193541970931834739735952393
# Kerberos流程中涉及的一些全局变量
# 由AS发给C的票据
global TGT
# C和TGS通信要用到的对称密钥
global EKc_tgs
# 由TGS发给C的票据
global ST
# C和S通信要用到的对称密钥
global EKc_v


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class Dialog(demo_manager_Dialog.Ui_Dialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.setupUi(self)


class Reader_Logic(demo_manager_MainWindow.Ui_MainWindow, demo_manager_Dialog.Ui_Dialog):
    def __init__(self):
        super(Reader_Logic, self).__init__()
        # 创建socket
        self.socket = None

    # 向AS发送注册消息
    def generate_msg_to_AS_register(self, src, result, target, ID_c, ID_pw, n, e):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': RSA_call({'ID_c': ID_c, 'ID_pw': ID_pw, 'RSA_n': n, 'RSA_e': e}, AS_n, AS_e, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': RSA_call({'ID_c': ID_c, 'ID_pw': ID_pw, 'RSA_n': n, 'RSA_e': e}, AS_n, AS_e, 0),
                          'HMAC': RSA_call(HMAC, C_n_1, C_d_1, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    # 向TGS发送注册消息
    def generate_msg_to_TGS_register(self, src, result, target, ID_c, n, e):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': RSA_call({'ID_c': ID_c, 'RSA_n': n, 'RSA_e': e}, TGS_n, TGS_e, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': RSA_call({'ID_c': ID_c, 'RSA_n': n, 'RSA_e': e}, TGS_n, TGS_e, 0),
                          'HMAC': RSA_call(HMAC, C_n_1, C_d_1, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    # 向S发送注册消息
    def generate_msg_to_S_register(self, src, result, target, ID_c, n, e):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': RSA_call({'ID_c': ID_c, 'RSA_n': n, 'RSA_e': e}, S_n, S_e, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': RSA_call({'ID_c': ID_c, 'RSA_n': n, 'RSA_e': e}, S_n, S_e, 0),
                          'HMAC': RSA_call(HMAC, C_n_1, C_d_1, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_AS_Kerberos(self, src, result, target, ID_c, ID_tgs, TS_1):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': {'ID_c': ID_c, 'ID_tgs': ID_tgs, 'TS_1': TS_1}}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_c': ID_c, 'ID_tgs': ID_tgs, 'TS_1': TS_1},
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_TGS_Kerberos(self, src, result, target, ID_v, Ticket_tgs, ID_c, AD_c, TS_3):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': {'ID_v': ID_v, 'ticket_TGS': Ticket_tgs,
                                        'Authenticator': DES_call(
                                            json.dumps({'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_3}),
                                            EKc_tgs, 0)}}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ID_v': ID_v, 'tick_tgs': TGT,
                                       'Authenticator': DES_call(json.dumps({'ID_c': ID_c, 'AD_c': AD_c, 'TS_3': TS_3}),
                                                                 EKc_tgs, 0)},
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Kerberos(self, src, result, target, Ticket_v, ID_c, AD_c, TS_5):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': {'tick_v': Ticket_v,
                                        'Authenticator': DES_call(
                                            json.dumps({'ID_c': ID_c, 'AD_c': AD_c, 'TS_5': TS_5}),
                                            EKc_v, 0)}}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': {'ticket_V': ST,
                                       'Authenticator': DES_call(json.dumps({'ID_c': ID_c, 'AD_c': AD_c, 'TS_5': TS_5}),
                                                                 EKc_v, 0)},
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Search(self, src, result, target, content):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': DES_call(json.dumps({'book_content': content}), EKc_v, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': DES_call({'book_content': content}, EKc_v, 0),
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Add(self, src, result, target, book_id, book_name, book_author, book_press, book_totalnum):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': DES_call(
                               json.dumps({'book_id': book_id, 'book_name': book_name, 'book_author': book_author,
                                           'book_press': book_press, 'book_totalnum': book_totalnum}), EKc_v, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': DES_call(
                              json.dumps({'book_id': book_id, 'book_name': book_name, 'book_author': book_author,
                                          'book_press': book_press, 'book_totalnum': book_totalnum}), EKc_v, 0),
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Modify(self, src, result, target, book_id, book_name, book_author, book_press, book_totalnum):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': DES_call(
                               json.dumps({'book_id': book_id, 'book_name': book_name, 'book_author': book_author,
                                           'book_press': book_press, 'book_totalnum': book_totalnum}), EKc_v, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': DES_call({'book_id': book_id}, EKc_v, 0),
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def generate_msg_to_S_Del(self, src, result, target, book_id):
        dict_msg_origin = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                           'data_msg': DES_call({'book_id': book_id}, EKc_v, 0)}
        str_msg_origin = json.dumps(dict_msg_origin)
        HMAC = generate_password_hash(str_msg_origin)
        dict_msg_final = {'control_msg': {'control_src': src, 'control_result': result, 'control_target': target},
                          'data_msg': DES_call({'book_id': book_id}, EKc_v, 0),
                          'HMAC': RSA_call(HMAC, C_n_2, C_d_2, 0)}
        str_msg_final = json.dumps(dict_msg_final)
        self.textBrowser_showtext.append(str_msg_final)
        return str_msg_final

    def C_AS_Register(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((AS_IP, AS_Port))
        ###
        print('选择了注册')
        ###
        try:
            # 发送数据
            send_data = self.generate_msg_to_AS_register('00', '0', '00000', str(self.lineEdit_username.text()),
                                                         str(self.lineEdit_passwd.text()), C_n_1, C_e_1)
            self.socket.sendall(send_data.encode('utf-8'))
            ###
            print('数据已发送')
            ###
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                ###
                print('已收到数据')
                ###
                final_str_data = total_data.decode('utf-8')
                final_loads_data = json.loads(final_str_data)
                if final_loads_data['control_msg']['control_result'] == '0':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1),
                                                     final_dumps_data)
                    ###
                    print('哈希校验的结果为：', hash_check)
                    ###
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请注册！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                                QMessageBox.Yes)
                if final_loads_data['control_msg']['control_result'] == '1':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1),
                                                     final_dumps_data)
                    ###
                    print('哈希校验的结果为：', hash_check)
                    ###
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请注册！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                                QMessageBox.Yes)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def C_AS_Kerberos(self):
        ###
        print('向AS申请服务开始')
        ###
        global TGT
        global EKc_tgs
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((AS_IP, AS_Port))
        ###
        print('成功连接AS')
        ###
        try:
            # 发送数据
            send_data = self.generate_msg_to_AS_Kerberos('00', '0', '00011', str(self.lineEdit_username.text()), 'TGS',
                                                         datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.socket.sendall(send_data.encode('utf-8'))
            ###
            print('数据已发送')
            ###
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                # QApplication.processEvents()
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                ###
                print('已收到数据')
                print(total_data)
                print(total_data.decode('utf-8'))
                ###

                # 解密来自AS的消息
                final_str_data = total_data.decode('utf-8')
                final_loads_data = json.loads(final_str_data)

                ###
                # 收到来自AS的正确消息的情况
                if final_loads_data['control_msg']['control_result'] == '0':
                    final_str_data_data_msg = DES_call(final_loads_data['data_msg'], str(self.lineEdit_passwd.text()),
                                                       1)
                    final_loads_data_data_msg = json.loads(final_str_data_data_msg)
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': final_loads_data['data_msg']})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", "AS认证通过！", QMessageBox.Yes, QMessageBox.Yes)
                        TGT = final_loads_data_data_msg['data_msg']['ticket_TGS']
                        EKc_tgs = final_loads_data_data_msg['data_msg']['EKc_tgs']
                # 收到来自AS的错误消息的情况
                if final_loads_data['control_msg']['control_result'] == '1':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], AS_n, AS_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                                QMessageBox.Yes)
                ###
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def C_TGS_Kerberos(self):
        ###
        print('向TGS申请服务开始')
        ###
        global TGT
        global EKc_tgs
        global ST
        global EKc_v
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TGS_IP, TGS_Port))
        ###
        print('成功连接TGS')
        ###
        try:
            # 发送数据
            send_data = self.generate_msg_to_TGS_Kerberos('00', '0', '00100', 'S', TGT,
                                                          str(self.lineEdit_username.text()),
                                                          get_host_ip(),
                                                          datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.socket.sendall(send_data.encode('utf-8'))
            ###
            print('数据已发送')
            ###
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                ###
                print('已收到数据')
                ###
                final_str_data = total_data.decode('utf-8')
                final_loads_data = json.loads(final_str_data)
                if final_loads_data['control_msg']['control_result'] == '0':
                    final_str_data_data_msg = DES_call(final_loads_data['data_msg'], EKc_tgs, 1)
                    final_loads_data_data_msg = json.loads(final_str_data_data_msg)
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': final_loads_data['data_msg']})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], TGS_n, TGS_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", "TGS认证通过！", QMessageBox.Yes, QMessageBox.Yes)
                        ST = final_loads_data_data_msg['data_msg']['ticket_V']
                        EKc_v = final_loads_data_data_msg['data_msg']['EKc_v']
                if final_loads_data['control_msg']['control_result'] == '1':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], TGS_n, TGS_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                                QMessageBox.Yes)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def C_S(self):
        ###
        print('向S申请服务开始')
        ###
        global ST
        global EKc_v
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((S_IP, S_Port))
        ###
        print('成功连接S')
        ###
        TS_5_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # 发送数据
            send_data = self.generate_msg_to_S_Kerberos('00', '0', '00101', ST, str(self.lineEdit_username.text()),
                                                        get_host_ip(), TS_5_str)
            self.socket.sendall(send_data.encode('utf-8'))
            ###
            print('数据已发送')
            ###
            # 接收数据,将收到的数据拼接起来
            total_data = bytes()
            while True:
                recv_data = self.socket.recv(1024)
                total_data += recv_data
                if len(recv_data) < 1024:
                    break
            if total_data:
                ###
                print('已收到数据')
                ###
                final_str_data = total_data.decode('utf-8')
                final_loads_data = json.loads(final_str_data)
                if final_loads_data['control_msg']['control_result'] == '0':
                    final_str_data_data_msg = DES_call(final_loads_data['data_msg'], EKc_v, 1)
                    final_loads_data_data_msg = json.loads(final_str_data_data_msg)
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': final_loads_data['data_msg']})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        TS_6_str = final_loads_data_data_msg['data_msg']['TS_6']
                        TS_6_dt = datetime.strptime(TS_6_str, '%Y-%m-%d %H:%M:%S')
                        TS_5_dt = datetime.strptime(TS_5_str, '%Y-%m-%d %H:%M:%S')
                        if TS_5_dt + timedelta(seconds=1) == TS_6_dt:
                            QMessageBox.information(self, "提示", "S认证通过！", QMessageBox.Yes, QMessageBox.Yes)

                            # 实例化一个对话框
                            dialog = Dialog()
                            dialog.exec_()

                        else:
                            QMessageBox.warning(self, "警告", "可能出现保文重放，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                if final_loads_data['control_msg']['control_result'] == '1':
                    final_dumps_data = json.dumps(
                        {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                         'control_result': final_loads_data['control_msg']['control_result'],
                                         'control_target': final_loads_data['control_msg']['control_target']},
                         'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                    hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                     final_dumps_data)
                    if not hash_check:
                        QMessageBox.warning(self, "警告", "消息可能被篡改，请重新申请认证！", QMessageBox.Yes, QMessageBox.Yes)
                    else:
                        self.textBrowser_showtext.append(final_str_data)
                        QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                                QMessageBox.Yes)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            self.socket.close()

    def Kerberos(self):
        self.C_AS_Kerberos()
        time.sleep(1)
        self.C_TGS_Kerberos()
        time.sleep(1)
        self.C_S()

    def C_S_Select(self, option):
        if option == 0:
            return self.generate_msg_to_S_Search('00', '0', '00110', str(self.lineEdit_content.text()))
        if option == 1:
            return self.generate_msg_to_S_Search('00', '0', '00111', str(self.lineEdit_content.text()))
        if option == 1:
            return self.generate_msg_to_S_Search('00', '0', '01000', str(self.lineEdit_content.text()))

    def C_S_Search(self):
        global EKc_v
        option = self.comboBox_select.currentIndex()
        # 发送数据
        send_data = self.C_S_Select(option)
        self.socket.sendall(send_data.encode('utf-8'))
        total_data = bytes()
        while True:
            recv_data = self.socket.recv(1024)
            total_data += recv_data
            if len(recv_data) < 1024:
                break
        if total_data:
            final_str_data = total_data.decode('utf-8')
            final_loads_data = json.loads(final_str_data)
            if final_loads_data['control_msg']['control_result'] == '0':
                final_str_data_data_msg = DES_call(final_loads_data['data_msg'], EKc_v, 1)
                final_loads_data_data_msg = json.loads(final_str_data_data_msg)
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': final_loads_data['data_msg']})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新搜索！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    newItem = QTableWidgetItem(final_loads_data_data_msg['data_msg']['book_id'])
                    self.tableWidget_result.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem(final_loads_data_data_msg['data_msg']['book_name'])
                    self.tableWidget_result.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem(final_loads_data_data_msg['data_msg']['book_author'])
                    self.tableWidget_result.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem(final_loads_data_data_msg['data_msg']['book_press'])
                    self.tableWidget_result.setItem(0, 3, newItem)
                    newItem = QTableWidgetItem(final_loads_data_data_msg['data_msg']['book_totalnum'])
                    self.tableWidget_result.setItem(0, 4, newItem)
            if final_loads_data['control_msg']['control_result'] == '1':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新搜索！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)

    def C_S_Add(self):
        global EKc_v
        send_data = self.generate_msg_to_S_Add('00', '0', '01100', str(self.lineEdit_book_id.text()),
                                               str(self.lineEdit_book_name.text()),
                                               str(self.lineEdit_book_author.text()),
                                               str(self.lineEdit_book_press.text()),
                                               str(self.lineEdit_book_totalnum.text()))
        self.socket.sendall(send_data.encode('utf-8'))
        total_data = bytes()
        while True:
            recv_data = self.socket.recv(1024)
            total_data += recv_data
            if len(recv_data) < 1024:
                break
        if total_data:
            final_str_data = total_data.decode('utf-8')
            final_loads_data = json.loads(final_str_data)
            if final_loads_data['control_msg']['control_result'] == '0':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新操作！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)
            if final_loads_data['control_msg']['control_result'] == '1':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新操作！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)

    def C_S_Modify(self):
        global EKc_v
        send_data = self.generate_msg_to_S_Modify('00', '0', '01101', str(self.lineEdit_book_id.text()),
                                                  str(self.lineEdit_book_name.text()),
                                                  str(self.lineEdit_book_author.text()),
                                                  str(self.lineEdit_book_press.text()),
                                                  str(self.lineEdit_book_totalnum.text()))
        self.socket.sendall(send_data.encode('utf-8'))
        total_data = bytes()
        while True:
            recv_data = self.socket.recv(1024)
            total_data += recv_data
            if len(recv_data) < 1024:
                break
        if total_data:
            final_str_data = total_data.decode('utf-8')
            final_loads_data = json.loads(final_str_data)
            if final_loads_data['control_msg']['control_result'] == '0':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新操作！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)
            if final_loads_data['control_msg']['control_result'] == '1':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新操作！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)

    def C_S_Del(self):
        global EKc_v
        send_data = self.generate_msg_to_S_Del('00', '0', '01011', str(self.lineEdit_book_id.text()))
        self.socket.sendall(send_data.encode('utf-8'))
        total_data = bytes()
        while True:
            recv_data = self.socket.recv(1024)
            total_data += recv_data
            if len(recv_data) < 1024:
                break
        if total_data:
            final_str_data = total_data.decode('utf-8')
            final_loads_data = json.loads(final_str_data)
            if final_loads_data['control_msg']['control_result'] == '0':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新操作！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)
            if final_loads_data['control_msg']['control_result'] == '1':
                final_dumps_data = json.dumps(
                    {'control_msg': {'control_src': final_loads_data['control_msg']['control_src'],
                                     'control_result': final_loads_data['control_msg']['control_result'],
                                     'control_target': final_loads_data['control_msg']['control_target']},
                     'data_msg': {'tips': final_loads_data['data_msg']['tips']}})
                hash_check = check_password_hash(RSA_call(final_loads_data['HMAC'], S_n, S_e, 1),
                                                 final_dumps_data)
                if not hash_check:
                    QMessageBox.warning(self, "警告", "消息可能被篡改，请重新操作！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", final_loads_data['data_msg']['tips'], QMessageBox.Yes,
                                            QMessageBox.Yes)


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = Reader_Logic()
    ui.show()
    sys.exit(app.exec_())
