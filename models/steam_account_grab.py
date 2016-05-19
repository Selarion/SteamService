# -*- coding: utf-8-*-
import base64
import json
import traceback
import urllib
import re
import time
import rsa

from grab import Grab


class SteamAccountGrab(Grab):
    def __init__(self, steam_account, login_steam, pass_steam, code_link):
        Grab.__init__(self)
        # self.base_page = BasePage(self)
        self.steam_account = steam_account
        self.login_steam = login_steam
        self.pass_steam = pass_steam
        self.code_link = code_link
        self.steam_id = None
        self.session_id = None

        cookiefile = '../cookies/' + login_steam + '.txt'
        self.setup(
            headers={
                'Accept': "text/javascript, text/html, application/xml, text/xml, */*",
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                'X-Prototype-Version': '1.7',
                'X-Requested-With': 'XMLHttpRequest'
            },
            cookiefile=cookiefile,
            reuse_cookies=True,
            debug_post=True,
            log_file='../log_steam_account/log_' + str(self.login_steam) + '.html'
        )

    def login(self):
        def login():
            def dict_to_string(body_request):
                a = urllib.urlencode(body_request)
                a = a.replace('+', '')
                a = a.replace("%27", "%22")
                a = a.replace('%25', '%')
                return a

            def get_auth_code():
                code_url = "http://localhost:3000" + self.code_link
                self.go(code_url)
                code = json.loads(self.response.body)
                return True, code["code"]

            def get_session_id():
                self.go('http://steamcommunity.com/')
                session_id = re.findall('g_sessionID = "(.+?)";', self.response.body)[0]
                return True, session_id

            def go_to_login_page():
                url = "https://steamcommunity.com/login/home/?goto=0"
                self.request(url=url)
                return True, None

            def get_mod_and_exp():
                body_request = {
                    'username': self.login_steam,
                    'donotcache': str(int(time.time() * 1000))
                }
                self.setup(url='https://steamcommunity.com/login/getrsakey/', post=body_request)
                self.request()
                str_response_body = self.response.body
                response_body = json.loads(str_response_body)
                self._flag_take_mod_and_exp = True
                return (
                    True,
                    response_body["publickey_mod"],
                    response_body['publickey_exp'],
                    response_body["timestamp"],
                )

            def get_enc_password(mod_and_exp):
                mod = long(mod_and_exp[0], 16)
                exp = long(mod_and_exp[1], 16)
                pub_key = rsa.PublicKey(mod, exp)
                crypto = rsa.encrypt(self.pass_steam, pub_key)
                enc_password = base64.b64encode(crypto)
                enc_password = enc_password.replace('+', '%2B')
                enc_password = enc_password.replace('/', '%2F')
                enc_password = enc_password.replace('=', '%3D')
                return True, enc_password

            def do_login(enc_password, timestamp, auth_code):
                body_request = {
                    'username': self.login_steam,
                    "password": enc_password,
                    "emailauth": "",
                    "twofactorcode": auth_code,
                    "loginfriendlyname": "",
                    "captchagid": "-1",
                    "captcha_text": "",
                    "emailsteamid": "",
                    "rsatimestamp": timestamp,
                    "remember_login": 'false',
                    "donotcache": str(int(time.time() * 1000))}

                body_request = dict_to_string(body_request)
                self.setup(url='https://steamcommunity.com/login/dologin/', post=body_request)
                self.request()
                str_response_body = self.response.body
                response_body = json.loads(str_response_body)
                print response_body

                if response_body['success'] is True:
                    self.steam_id = response_body['transfer_parameters']['steamid']
                    return True, None
                if response_body['message'] != '':
                    return False, response_body['message']

            flag_get_auth_code = False
            flag_get_session_id = False
            flag_go_to_login_page = False
            flag_get_mod_and_exp = False
            flag_get_enc_password = False
            flag_do_login = False
            error_message = None
            login_error_counter = 0
            while login_error_counter < 3:
                try:
                    if not flag_get_auth_code:
                        flag_get_auth_code, auth_code = get_auth_code()
                        continue
                    if not flag_get_session_id:
                        flag_get_session_id, self.session_id = get_session_id()
                        continue
                    if not flag_go_to_login_page:
                        flag_go_to_login_page = go_to_login_page()
                        continue
                    if not flag_get_mod_and_exp:
                        answer = get_mod_and_exp()
                        flag_get_mod_and_exp = answer[0]
                        mod_and_exp = answer[1:3]
                        timestamp = answer[3]
                        continue
                    if not flag_get_enc_password:
                        flag_get_enc_password, enc_password = get_enc_password(mod_and_exp)
                    if not flag_do_login:
                        flag_do_login, error_message = do_login(enc_password, timestamp, auth_code)
                        if error_message:
                            return False, error_message
                    return True, None
                except StandardError:
                    error_message = traceback.format_exc()
                    login_error_counter += 1
                    time.sleep(5)
            return False, error_message
        return login()

    def logout(self):
        try:
            self.setup(url='https://steamcommunity.com/login/logout/', post={"sessionid": self.session_id})
            self.request()
        except StandardError:
            pass

    def get_sessionid(self):
        return self.session_id
