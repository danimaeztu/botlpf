# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:56:48 2019

@author: Daniel Maeztu
http://danimaeztu.com
version: 4.4
"""
from datetime import datetime
import pandas as pd
import sqlalchemy
import tweepy
import psutil
import config as cf


def logger(tw):
    """Feed a log"""
    sql = """INSERT INTO log (timestamp, tweet, CPU, RAM)
        VALUES ("{}", "{}", "{}", "{}");""".format(now.strftime('%d-%m-%Y %H:%M:%S'),
                                                   tw,
                                                   psutil.cpu_percent(),
                                                   psutil.virtual_memory().percent)
    connection.execute(sql)


def composer(x):
    """Compose the tweet"""
    tweet = "Tal día como hoy, hace {} años, {} posteó: {} {} {}".format(
            int(now_ano) - int(x['ano']),
            x['twitter'],
            x['titulo'],
            x['tags'],
            x['url']
            )
    api.update_status(tweet)
    cf.tweet = tweet


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
sql = """SELECT * FROM posts_min
      WHERE fecha = "{}"
      AND hora = "{}";""".format(now_fecha, now_hora)
result = pd.read_sql(sql, connection)

# Execute
result.apply(composer, axis=1)  # If there are no results it will do nothing

# log
logger(cf.tweet)

# Aniversaries
aniversary("04-24", "21:54",
           tw=f"Tal día como hoy, hace {int(now_ano) - 2009} años se puso en marcha esta cuenta de Twitter. ¡Celebrémoslo!")
aniversary("10-19", "18:28",
           tw=f"Tal día como hoy, hace {int(now_ano) - 2019} años comenzó a ejecutarse el botlpf ¡Cuántos buenos momentos desde entonces!")

connection.close()
