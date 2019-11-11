# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:56:48 2019

@author: Daniel Maeztu
http://danimaeztu.com
"""
import pandas as pd
from apiclient.discovery import build
import sqlalchemy
import config


# New columns functions to use with pandas "apply"
def tstofecha(x):
    """Timestamp to date (month-day)"""
    return(x[5:10])


def tstoano(x):
    """Timestamp to year"""
    return(x[0:4])


def tstohora(x):
    """Timestamp to hour"""
    return(x[11:16])


def etiquetatotag(x):
    """Blogger tags to Twitter tags"""
    tags = ['#LPF']
    if x != 'None':
        for i in x:
            i = i.replace(' ', '')
            tags.append("#"+i)
    tags = (" ".join(tags))
    return(tags)


# Blogger API connection
service = build('blogger', 'v3', developerKey=config.developerKey)
posts = service.posts()

# Mysql connection and create schema and tables
mysql = "mysql://{}:{}@{}".format(
        config.sql_user, config.sql_pw, config.sql_host)
engine = sqlalchemy.create_engine(mysql)
connection = engine.connect()

with open('{}\\create_tables.sql'.format(config.path), 'r') as file:
    sql = file.read()
    connection.execute(sql)

# Initialize some arguments
pageToken = None
datos = []

# Obtain full data from target blog
while pageToken is not False:
    data = posts.list(blogId=config.blogId, pageToken=pageToken).execute()
    for item in data['items']:
        autor = item['author']['displayName']
        titulo = item['title']
        url = item['url']
        timestamp = item['published']
        post = item['content']
        comentarios = item['replies']['totalItems']
        try:
            etiquetas = item['labels']
        except(KeyError):
            etiquetas = 'None'
        line = [titulo, autor, timestamp, url, post, etiquetas, comentarios]
        datos.append(line)
    try:
        pageToken = data['nextPageToken']
    except(KeyError):
        pageToken = False

# Create pandas DataFrame from a list of lists
data = pd.DataFrame(datos,
                    columns=['titulo', 'autor', 'timestamp', 'url', 'post',
                             'etiquetas', 'comentarios'])

# New colummns
data['fecha'] = data['timestamp'].apply(tstofecha)
data['hora'] = data['timestamp'].apply(tstohora)
data['ano'] = data['timestamp'].apply(tstoano)
data['tags'] = data['etiquetas'].apply(etiquetatotag)

twitterusers = pd.read_csv('{}\\csv\\Twitter_users.csv'.format(config.path),
                           encoding='latin_1')
data = pd.merge(data, twitterusers, on='autor', how='left')

# CSV and MySql posts_full
data.to_csv('{}\\csv\\posts_full.csv'.format(config.path), index=False)
data.to_sql('posts_full', con=connection, schema='botlpf_test',
            if_exists='append', index=False)

# Just the minimum data
data = data[['titulo', 'url', 'ano', 'fecha', 'hora', 'twitter', 'tags']]

data.to_csv('{}\\csv\\posts_min.csv'.format(config.path), index=False)
data.to_sql('posts_min', con=connection, schema='botlpf_test',
            if_exists='append', index=False)
