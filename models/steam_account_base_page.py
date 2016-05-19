# -*- coding: utf-8-*-


class BasePage:
    def __init__(self, grab):
        self.grab = grab

    def check_login(self):
        return self.grab.doc.select(".//*[@id='global_actions']/a/img").exists()

    def refresh_page(self):
        self.grab.refresh()
        return self.check_login()
