from flask import Flask

import configuration

app = Flask(__name__)
app.config.from_object(configuration.DevelopmentConfig)
app.config['SECRET_KEY'] = 'secret_key'

from app import routes