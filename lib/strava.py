import requests
from bs4 import BeautifulSoup

__version__ = "0.0.1"

class Strava:

    strava_cookie_name = "_strava4_session"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.loggedIn = False
        self.cookies = {
            self.strava_cookie_name : ""
        }
        self.headers = {
            'User-agent' : 'SocMySport ' + __version__,
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        self.weekDistance = ""
        self.unit = ""
        self.yearDistance = ""

    def presenter(self):
        return "Email is: " + self.email + ", password is #########"

    def login(self):
        login = requests.get('https://www.strava.com/login', headers = self.headers)
        html = login.text
        doc = BeautifulSoup(html, features='lxml')

        element = doc.find('meta', attrs={'name':'csrf-token'})
        if element.attrs['content'] != "":
            authenticity_token = element.attrs['content']
        else:
            return False

        for cookie in login.cookies:
            if cookie.name == self.strava_cookie_name:
                self.cookies[self.strava_cookie_name] = cookie.value

        self.headers['Referer'] = 'https://www.strava.com/login'

        payload = {
            'authenticity_token' : authenticity_token,
            'utf8' : '✓',
            'plan' : '',
            'email': self.email,
            'password' : self.password,
            'remember_me': 'on'
        }

        session = requests.post('https://www.strava.com/session', data = payload, headers = self.headers, cookies = self.cookies)
        for cookie in session.cookies:
            if cookie.name == self.strava_cookie_name:
                self.cookies[self.strava_cookie_name] = cookie.value

        doc = BeautifulSoup(session.text, features='lxml')
        for element in doc.find('span', attrs={'class':'actual'}):
            elementInfo = element.split()
            self.weekDistance = elementInfo[0]
            self.unit = elementInfo[1]

        self.loggeIn = True
        return True

    def getWeekDistance(self):
        if self.loggedIn == False:
            if self.login() == False:
                return "0.00"
        return self.weekDistance

    def getYearDistance(self):
        if self.loggedIn == False:
            if self.login() == False:
                return "0.00"
        calendar = requests.get('https://www.strava.com/athlete/calendar', headers = self.headers, cookies = self.cookies )
        doc = BeautifulSoup(calendar.text, features='lxml')
        for element in doc.find('script', attrs={'id' : 'year-stats-template'}):
            year_stats = element

        doc = BeautifulSoup(year_stats, features='lxml')
        for element in doc.find('a', attrs={'data-view-type' : 'distance'}):
            if element.name == 'strong':
                self.yearDistance = element.string
        return self.yearDistance
