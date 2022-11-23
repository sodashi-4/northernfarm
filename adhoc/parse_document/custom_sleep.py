from time import sleep
from random import uniform

def short_sleep():
    sleep(uniform(2, 3))

def medium_sleep():
    sleep(uniform(7, 10))

def long_sleep():
    sleep(uniform(30, 40))