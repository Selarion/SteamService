# -*- coding: utf-8-*-
import Queue
import json
import threading

from grab import error
from grab import Grab
import re
import time
from controllers.steam_account_controller import SteamAccountController

import logging
logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class SteamAccount(Grab):
    def __init__(self, login_steam, pass_steam, code_link):
        Grab.__init__(self)

        self.controller = SteamAccountController(self)
        self.steam_account_controller_thread = threading.Thread(target=self.controller.start_route,
                                                                name="%s SteamAccountControllerThread" % login_steam)
        self.login_steam = login_steam
        self.pass_steam = pass_steam
        self.code_link = code_link

        self.steam_id = None
        self.session_id = None

        headers = {
            'Accept': "text/javascript, text/html, application/xml, text/xml, */*",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest'
        }
        cookiefile = '../cookies/'+login_steam+'.txt'
        self.setup(headers=headers,
                   cookiefile=cookiefile,
                   reuse_cookies=True,
                   debug_post=True,
                   log_file='../log_steam_account/log_'+str(self.login_steam)+'.html')

    def start(self, output_queue):
        print "Steam account %s is start!" % self.login_steam
        self.controller.set_output_queue(output_queue)
        self.steam_account_controller_thread.start()
        if self.login():
            print 'login sucsess'
            self.start_main_event_loop()
        else:
            print 'login not sucsess'

    def login(self):
        def login():
            def take_code():
                try:
                    code_url = "http://localhost:3000"+self.code_link
                    self.go(code_url)
                    try:
                        auth_code = json.loads(self.response.body)
                        return False, auth_code["message"]
                    except Exception:
                        auth_code = self.response.body
                        return True, auth_code
                except error.GrabError:
                    return False, 'Error: GrabError in step "take_code"'

            def session_id():
                try:
                    self.go('http://steamcommunity.com/')
                    session_id = re.findall('g_sessionID = "(.+?)";', self.response.body)[0]
                    return True, session_id
                except Exception:
                    time.sleep(1)
                    return False, None

            def go_to_login_page():
                try:
                    url = "https://steamcommunity.com/login/home/?goto=0"
                    self.request(url=url)
                    return True, None
                except error.GrabError:
                    return False, 'Error: GrabError in step "take_code"'

            def mod_and_exp():
                pass

            def enc_password():
                pass

            def dologin():
                pass

            flag_take_code = False
            flag_session_id = False
            flag_go_to_login_page = False
            flag_take_mod_and_exp = False
            flag_enc_password = False
            flag_first_dologin = False

            flag_second_dologin = False
            flag_login_finish = False
            login_error = 0
            while login_error < 3:
                if not flag_take_code:
                    flag_take_code, code = take_code()
                    continue
                if not flag_session_id:
                    flag_session_id, self.session_id = session_id()
                    continue
                if not flag_go_to_login_page:
                    flag_go_to_login_page, error_massage = go_to_login_page()
                    continue


                raw_input(self.session_id)

            return False
        return login()

    def start_main_event_loop(self):
        while True:
            pass

if __name__ == '__main__':
    sa = SteamAccount(login_steam='stl_postman_2', pass_steam='OoV3nNob', code_link='/bot/?id=2')
    if sa.login():
        print 'login sucsess'
    else:
        print 'login not sucsess'
