from flask import Flask, request, session, redirect, url_for, escape, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

config = DevelopmentConfig

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

import models
from views import admin
from views import api
from views import account


@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('account_login'))
    else:
        return redirect(url_for('account_profile'))

@app.route('/admin')
def admin_index():
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_dashboard'))




