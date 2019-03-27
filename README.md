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
You have to create a twitter developper account and get your own consumer_key and consumer_secret credentials. You can follow the process described on the twurl page to do so: https://github.com/twitter/twurl#getting-started.

## Installation
Grab a copy of the config file in the example folder and place it under
```
$HOME/.config/SocMySport/config.txt
```
Set the variables to real values.

## Variable replacement
In the *name* variable, &lt;week_distance&gt; will be replaced by your weekly cycled distance.

In the *profile*, &lt;year_distance&gt; will be replaced by your yearly cycled distance, and &lt;CO2&gt; by the amount of CO₂ you saved! (don't forget to correctly set the *fuelconsumption* and *co2perunit* variables)

## Run
Execute:
```
python3 socMySport.py
```
## Automate
Add the above command to your crontab :)
