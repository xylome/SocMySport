#!/usr/bin/env python3

__author__ = "Xavier Héroult <xavier@placard.fr.eu.org>"
__copyright__ = "Copyright 2019, Xavier Héroult"
__credits__ = ["Xavier Héroult"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Xavier Héroult"
__email__ = "xavier@placard.fr.eu.org"
__status__ = "Prototype"

import os, sys
from os.path import expanduser, dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), 'lib')))

import configparser
import twitter

from strava import Strava

home = expanduser('~')
CONF_FILE = home + '/.config/SocMySport/config.txt'


def getCO2(distance, co2perunit, fuelconsumption):
    distanceFloat = float(distance.replace(',', '.').replace('\xa0', ''))
    fuelconsumptionFloat = float(fuelconsumption)
    co2perunitFloat = float(co2perunit)
    usedFuelFor100 = distanceFloat * fuelconsumptionFloat
    usedFuel = usedFuelFor100 / 100.0
    co2 = usedFuel * co2perunitFloat
    return '{:03.2f}'.format(co2).replace('.', ',')


try:
    conf_stat = os.stat(CONF_FILE)
except FileNotFoundError as e:
    print('Fichier de conf', CONF_FILE, 'introuvable. --', e)
    exit(1)

try:
    config = configparser.RawConfigParser()
except BaseException as e:
    print('fichier pas au bon format.', e)
    exit(2)

try:
    config.read(CONF_FILE)
except:
    print('fichier pas au bon format')
    exit(3)

try:
    name = config.get('general', 'name')
    profile = config.get('general', 'profile')
    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')
    access_token_key = config.get('twitter', 'access_token_key')
    access_token_secret = config.get('twitter', 'access_token_secret')
    strava_login = config.get('strava', 'login')
    strava_password = config.get('strava', 'password')
    co2perunit = config.get('general', 'co2perunit')
    fuelconsumption = config.get('general', 'fuelconsumption')
except BaseException as e:
    print('il manque des choses dans la conf, vérifiez.', e)
    exit(4)

strava_user = Strava(strava_login, strava_password)
twitter_user = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                           access_token_key=access_token_key, access_token_secret=access_token_secret)

new_name = name.replace('<week_distance>', strava_user.getWeekDistance() + ' ' + strava_user.unit)
print('Will set name to:', new_name)

if len(profile) > 1:
    year_distance = strava_user.getYearDistance()
    profile = profile.replace('<year_distance>', year_distance + ' ' + strava_user.unit)
    profile = profile.replace('<CO2>', getCO2(year_distance, co2perunit, fuelconsumption))
    print('Will set profile to:', profile)
    twitter_user.UpdateProfile(name=new_name, description=profile)
else:
    twitter_user.UpdateProfile(name=new_name)
