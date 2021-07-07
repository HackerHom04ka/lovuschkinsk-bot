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
    "token": "1d72e176625cfa8949dc1a36657ffdfaf4b82fa3e12adeae487587f8ba9640f3df876a069c375f04cc40b",
    'admin_ids': [578425189, 541179325, 325809318, 620261037, 632017862],
    "token_papochka": "5b8b8d17d60201c281e18906391cdb4bc18f79591883db7e79a749069a95f195483f920d31f8e21579b4d"
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
