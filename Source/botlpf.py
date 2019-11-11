# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:56:48 2019

@author: Daniel Maeztu
http://danimaeztu.com
version: 4.2
"""
from datetime import datetime
import pandas as pd
import sqlalchemy
import tweepy
import config


def logger(tw):
    """Feed a log"""
    sql = """INSERT INTO log (timestamp, tweet)
        VALUES ("{}", "{}");""".format(now.strftime('%d-%m-%Y %H:%M:%S'), tw)
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
    config.tweet = tweet


# Set current time and date
now = datetime.now()
now_fecha = now.strftime("%m-%d")
now_hora = now.strftime("%H:%M")
now_ano = now.strftime("%Y")

# Connection to Mysql
mysql = "mysql://{}:{}@localhost/botlpf".format(
        config.sql_user, config.sql_pw)
engine = sqlalchemy.create_engine(mysql)
connection = engine.connect()

# Connection to Twitter
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

# Load the posts table
sql = """SELECT * FROM posts_min
      WHERE fecha = "{}"
      AND hora = "{}";""".format(now_fecha, now_hora)
result = pd.read_sql(sql, connection)

# Execute
result.apply(composer, axis=1)  # If there are no results it will do nothing

# log
logger(config.tweet)
