__all__ = ('app', 'twitter', 'mongo')

from flask import Flask
from flask.ext.tweepy import Tweepy
from flask.ext.pymongo import PyMongo
from os.path import abspath, dirname, exists, join

app = Flask(__name__)

here = dirname(__file__)
parent = abspath(join(dirname(__file__), '..'))

config = join(parent, 'pyq.cfg')
if exists(config):
    app.config.from_pyfile(config)

private = join(parent, 'private.pyq.cfg')
if exists(private):
    app.config.from_pyfile(private)

twitter = Tweepy(app)
mongo = PyMongo(app)

import pythonquestions.views

