#!/usr/bin/env python3

__author__     = "Xavier Héroult <xavier@placard.fr.eu.org>"
__copyright__  = "Copyright 2019, Xavier Héroult"
__credits__    = ["Xavier Héroult"]
__license__    = "GPL"
__version__    = "1.0.0"
__maintainer__ = "Xavier Héroult"
__email__      = "xavier@placard.fr.eu.org"
__status__     = "Prototype"

import os
from os.path import expanduser

import configparser
import requests
from bs4 import BeautifulSoup

import twitter

home = expanduser("~")
CONF_FILE = home + "/.config/SocMySport/config.txt"

strava_cookie_name = '_strava4_session'
headers = {
    'User-agent' : 'SocMySport ' + __version__,
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
}
cookies = {
    strava_cookie_name : ""
}

try:
    conf_stat = os.stat(CONF_FILE)
except FileNotFoundError as e:
    print("Fichier de conf", CONF_FILE, "introuvable. --", e)
    exit(1)

try:
    config = configparser.RawConfigParser()
except BaseException as e:
    print("fichier pas au bon format.", e)
    exit(2)

try:
    config.read(CONF_FILE)
except:
    print("fichier pas au bon format")
    exit(3)

try:
    name = config.get('general', 'name')
    profile = config.get('general', 'profile')
    consumer_key = config.get("twitter", "consumer_key")
    consumer_secret = config.get("twitter", "consumer_secret")
    access_token_key = config.get("twitter", "access_token_key")
    access_token_secret = config.get("twitter", "access_token_secret")
    strava_login = config.get("strava", "login")
    strava_password = config.get("strava", "password")
except BaseException as e:
    print("il manque des choses dans la conf, vérifiez.", e)
    exit(4)

login = requests.get('https://www.strava.com/login', headers = headers)
html = login.text
doc = BeautifulSoup(html, features='lxml')

element = doc.find('meta', attrs={'name':'csrf-token'})
if element.attrs['content'] != "":
    authenticity_token = element.attrs['content']
else:
    print("No authenticity_token found, exiting.")
    exit(10)

for cookie in login.cookies:
    cookies[strava_cookie_name] = cookie.value

headers['Referer'] = 'https://www.strava.com/login'

payload = {
    'authenticity_token' : authenticity_token,
    'utf8' : '✓',
    'plan' : '',
    'email': strava_login,
    'password' : strava_password,
    'remember_me': 'on'
}

session = requests.post('https://www.strava.com/session', data = payload, headers = headers, cookies = cookies)
for cookie in session.cookies:
    if cookie.name == strava_cookie_name:
        cookies[strava_cookie_name] = cookie.value

doc = BeautifulSoup(session.text, features='lxml')
for element in doc.find('span', attrs={'class':'actual'}):
    distance = element

new_name = name.replace("<week_distance>", distance)
print("Will set name to:", new_name)

if len(profile) > 1:
    calendar = requests.get('https://www.strava.com/athlete/calendar', headers = headers, cookies = cookies )
    doc = BeautifulSoup(calendar.text, features='lxml')
    for element in doc.find('script', attrs={'id' : 'year-stats-template'}):
        year_stats = element

    year_distance = ""
    doc = BeautifulSoup(year_stats, features='lxml')
    for element in doc.find('a', attrs={'data-view-type' : 'distance'}):
        if element.name == 'strong' or element.name == 'div':
            year_distance += element.string + ' '
    profile = profile.replace("<year_distance>", year_distance.strip())
    print("Will set profile to:", profile)

api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret,
                    access_token_key = access_token_key, access_token_secret = access_token_secret)

if len(year_distance) > 0:
    api.UpdateProfile(name = new_name, description = profile)
else:
    api.UpdateProfile(name = new_name)
print("Done.")
