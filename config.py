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
    "token": "f6bb39939051686173c4ec3dde30be7df36af7cf07b3700d660a6be5cdc750dd3df5f36c0d96baafc45ad",
    'admin_ids': [578425189, 632017862, 507603326, 325809318, 620261037],
    "token_papochka": "a4f28407db73134f0c4831506bc7b89ff7561ec95b2c5d245fa455f417904de394d9bb24de83140e23f46"
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
