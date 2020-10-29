from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from vk_api import vk

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
    'admin_ids': [578425189]
}

app.config['DEBUG'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jgebkzqmdypmnn:dbe08c523f1f2d4b125bd332a022cdf72c93a9551041fcbdb71fb7bb3b05ff13@ec2-52-72-34-184.compute-1.amazonaws.com:5432/d21fpmusudrt7o'

db = SQLAlchemy(app)

session = vk(group_config['token'])