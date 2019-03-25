# SocMySport
Python script to add your weekly cycled distance (from strava) to your twitter name.
Now add your yearly cycled distance to your twitter profile.

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

The *name* variable will be parsed to replace &lt;week_distance&gt; by your weekly cycled distance. The *profile* variable will be parsed to replace &lt;year_distance&gt; by your yearly cycled distance. NB: you can set the *profile* variable to empty string if you don't want to update your profile, but the variable has to be present in the configuration file.
## Run
Execute:
```
python3 socMySport.py
```
## Automate
Add the above command to your crontab :)
