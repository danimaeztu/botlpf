# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:56:48 2019

@author: Daniel Maeztu
http://danimaeztu.com
version: 4.5.3
"""
from datetime import datetime
import os
import pandas as pd
import sqlalchemy
import tweepy
import psutil
from jinja2 import Template
import config as cf


def logger(tw):
    """Feed a log.
    Send notice mail message if cpu or ram overload.
    """
    cpu_load = psutil.cpu_percent()
    ram_load = psutil.virtual_memory().percent
    with open(f'{cf.templates_path}/log_insert.sql') as f:
        tm = Template(f.read())
    sql = tm.render(timestamp=now.strftime('%d-%m-%Y %H:%M:%S'),
                    tweet=tw,
                    cpu_load=cpu_load,
                    ram_load=ram_load)
    connection.execute(sql)
    if cpu_load>99 or ram_load>99:
        with open(f'{cf.templates_path}/mail_overload.txt') as f:
            tm = Template(f.read())
        body = tm.render(timestamp=now.strftime('%Y-%m-%d %H:%M:%S'),
                        cpu_pct=cpu_load,
                        ram_pct=ram_load)
        os.system(f"echo '{body}' | mail -s 'danimaeztu.com: Server overload' {cf.mail}")


def composer(x):
    """Compose the tweet"""
    with open(f'{cf.templates_path}/tweet01.txt') as f:
        tm = Template(f.read())
    tweet = tm.render(years=int(now_ano)-int(x['ano']),
                    user=x['twitter'],
                    title=x['titulo'],
                    tags=x['tags'],
                    url=x['url'])
    api.update_status(tweet)
    cf.tweet = '"' + tweet.replace('"', '') + '"'


def aniversary(fecha, hora, tw):
    """Easter egg"""
    if now_fecha == fecha and now_hora == hora:
        api.update_status(tw)
        logger(tw)


# Set current time and date
now = datetime.now()
now_fecha = now.strftime("%m-%d")
now_hora = now.strftime("%H:%M")
now_ano = now.strftime("%Y")

# Connection to Mysql
mysql = "mysql://{}:{}@localhost/botlpf".format(
        cf.sql_user, cf.sql_pw)
engine = sqlalchemy.create_engine(mysql)
connection = engine.connect()

# Connection to Twitter
auth = tweepy.OAuthHandler(cf.consumer_key, cf.consumer_secret)
auth.set_access_token(cf.access_token, cf.access_token_secret)
api = tweepy.API(auth)

# Load the posts table
with open(f'{cf.templates_path}/post_select.sql') as f:
    tm = Template(f.read())
sql = tm.render(date=now_fecha,
                time=now_hora)
result = pd.read_sql(sql, connection)

# Execute
result.apply(composer, axis=1)  # If there are no results it will do nothing
# log
logger(cf.tweet)

# Aniversaries
aniversary("04-24", "21:54",
           tw=f"Tal día como hoy, hace {int(now_ano)-2009} años se puso en marcha esta cuenta de Twitter. ¡Celebrémoslo!")
aniversary("10-19", "18:28",
           tw=f"Tal día como hoy, hace {int(now_ano)-2019} años comenzó a ejecutarse el botlpf ¡Cuántos buenos momentos desde entonces!")

connection.close()
