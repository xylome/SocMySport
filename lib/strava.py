import os

import requests
from bs4 import BeautifulSoup

__version__ = "0.0.1"


class Strava:
    strava_cookie_name = "_strava4_session"
    verify = True

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.loggedIn = False
        self.cookies = {

        }
        self.headers = {
            'user-agent' : 'pylibstrava  ' + __version__,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
        }
        self.weekDistance = ""
        self.unit = ""
        self.yearDistance = ""

    def presenter(self):
        return "Email is: " + self.email + ", password is #########"

    def login(self):
        login = requests.get('https://www.strava.com/login', headers=self.headers, verify=self.verify)
        html = login.text
        doc = BeautifulSoup(html, features='lxml')

        element = doc.find('meta', attrs={'name': 'csrf-token'})
        if element.attrs['content'] != "":
            authenticity_token = element.attrs['content']
        else:
            return False

        for cookie in login.cookies:
            if cookie.name == self.strava_cookie_name:
                self.cookies[self.strava_cookie_name] = cookie.value

        self.headers['referer'] = 'https://www.strava.com/login'

        payload = {
            'utf8': '✓',
            'authenticity_token': authenticity_token,
            'plan': '',
            'email': self.email,
            'password': self.password
        }

        session = requests.post('https://www.strava.com/session',
                                data=payload, headers=self.headers, cookies=self.cookies,
                                allow_redirects=False, verify=self.verify)
        if session.status_code == 302:
            self.cookies = session.cookies
            redirect_url = session.headers['Location']
            del self.headers['referer']
            self.headers['referer'] = 'https://www.strava.com/session'
        else:
            print("no redirect")
            return False

        dashboard = requests.get(redirect_url, headers=self.headers, cookies=self.cookies, verify=self.verify)

        doc = BeautifulSoup(dashboard.text, features='lxml')
        for element in doc.find('span', attrs={'class': 'actual'}):
            elementInfo = element.split()
            self.weekDistance = elementInfo[0]
            if len(elementInfo) == 2:
                self.unit = elementInfo[1]
            else:
                # The weekly goal is probably enabled, have to find unit in the next class
                for element in doc.find('span', attrs={'class': 'goal'}):
                    elementInfo = element.split()
                    if len(elementInfo) == 2:
                        self.unit = elementInfo[1]
                    else:
                        print("No information about distance unit, defaulting to km")
                        self.unit = "km"

        self.loggedIn = True
        return True

    def getWeekDistance(self):
        if not self.loggedIn:
            if not self.login():
                return "0.00"
        return self.weekDistance

    def getYearDistance(self):
        if not self.loggedIn:
            if not self.login():
                return "0.00"

        calendar = requests.get('https://www.strava.com/athlete/calendar', headers=self.headers, cookies=self.cookies,
                                verify=self.verify)
        doc = BeautifulSoup(calendar.text, features='lxml')
        for element in doc.find('script', attrs={'id': 'year-stats-template'}):
            year_stats = element

        doc = BeautifulSoup(year_stats, features='lxml')
        for element in doc.find('a', attrs={'data-view-type': 'distance'}):
            if element.name == 'strong':
                self.yearDistance = element.string
        return self.yearDistance
