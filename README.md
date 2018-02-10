# Cryptocurrency trading platform

Retrieves data using poloniex api.

### Availble:
* Control trading sessinon via Start and Stop buttons.
* Real time interactive chart with trading strategy executions.
* Real time updating table with opened postions and all trades.
* Trading history storing into csv file.
* Real time messages from exchange and from platform in console.

Easy to change trading logic, available different markets indicators to use in strategy module(botsrategy.py).
For using neccessary to have your own id and key from poloniex api.
<hr>

### Requiremets:
* python 3.6
* poloniex
* tkinter
* pandas
* cayons
* colorama

### Install latest poloniex api release:
```
pip install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.7.zip
```
### Usage:
```
import poloniex
polo = poloniex.Poloniex('your-Api-Key-Here-xxxx','yourSecretKeyHere123456789')
```
### Run application:
```From cmd:
python Gui.py
```
<hr>

### Trading example:

![alt text](https://user-images.githubusercontent.com/10981310/36055671-a45e4e42-0e06-11e8-9d3e-875830092582.PNG)
