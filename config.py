from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from vk_api import vk
from flask_migrate import Migrate

app = Flask('lovushkinsk')

try:
    confirm = os.environ['CONFIRM']
except:
    confirm = '00000000'

group_config = {
    "id": 193840305,
    "secret": "mjeynofbopn7t1j5aipm9ggxivjnxvq9",
    "confirm": confirm,
    "token": "3a11ee2eef165b831ea31253e369bfd4377f12fee98dcfbc11054655de7538485133a773c55cb1521aaae",
    'admin_ids': [578425189],
    "token_papochka": "414555006e083f8dbaff1d00db714fa35b6516789adda87ae428a541b8f6d5ef5a468cf0dff3ed7219a3b"
}

app.config['DEBUG'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kjnpwujmrlkrxf:a4749d1f7771f81a3e9b20eb8119ca92a27c1ef4192229e0145b3ece0bc29aff@ec2-107-22-33-173.compute-1.amazonaws.com:5432/djfr3k1op99nt'

db = SQLAlchemy(app)

session_papochka = vk(group_config['token_papochka'])
session = vk(group_config['token'])

migrate = Migrate(app, db)
