import hashlib
from mailapi import db, config
from collections import OrderedDict
import datetime


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    apikeys = db.relationship('AdminApikey', backref='admin')
    domains = db.relationship('Domain', backref='admin')

    def __init__(self, username, password_clear):
        self.username = username

        self.created = datetime.datetime.now()

        self.password = self.get_crypt_password(password_clear)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return_dict = OrderedDict()

        return_dict['id'] = self.id
        return_dict['username'] = self.username

        return return_dict

    def get_crypt_password(self, password_clear):
        password_hash = hashlib.sha512((self.created.isoformat() +
                                        password_clear +
                                        config.PASSWORD_PEPPER).encode())

        return password_hash.hexdigest()

    def check_password(self, password_clear):
        password_hash = self.get_crypt_password(password_clear)

        return password_hash == self.password