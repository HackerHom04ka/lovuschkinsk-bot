from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from vk_api import vk
from urllib.parse import urlparse

app = Flask('lovushkinsk')

try:
    confirm = os.environ['CONFIRM']
except:
    confirm = '00000000' # Ключ подтверждения

group_config = {
    "id": 193840305, # ID группы
    "secret": "xxx", # Секретный ключ. Оставить пустым, если не задан
    "confirm": confirm, # Ключ подтверждения
    "token": "xxx", # Токен группы
    'admin_ids': [578425189], # ID пользователей, которые админы
    "token_papochka": "xxx" # Токен одного из админов
}

app.config['DEBUG'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 3600,
    "max_overflow": 300
}
try:
    xi = urlparse(os.environ['DATABASE_URL'])
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://" + xi.username + ":" + xi.password + "@" + xi.hostname + ":" + xi.port + xi.path
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://username:password@host:port/db'

db = SQLAlchemy(app)

session_papochka = vk(group_config['token_papochka'])
session = vk(group_config['token'])
