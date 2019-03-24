# SocMySport
Python script to add your weekly cycled distance (from strava) to your twitter name.

## Dependencies
This script should be run with the version 3 of Python, with these libraries:
* configparser
* requests
* bs4
* python-twitter
* lxml

Install them with:
```
pip3 install "library_name"
```
## Prerequisites
You have to create a twitter developper account and get your own consumer_key and consumer_secret credentials. You can follow the process described on the twurl page to do so : https://github.com/twitter/twurl#getting-started.

## Installation
Grab a copy of the config file in the example folder and place it under
```
$HOME/.config/SocMySport/config.txt
```
Set the variables to real values.

The *name* variable will be parsed to replace &lt;distance&gt; by your weekly cycled distance.

## Run
Execute:
```
python3 SocMySport.py
```
## Automate
Add the above command to your crontab :)
