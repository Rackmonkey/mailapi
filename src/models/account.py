import hashlib
from mailapi import db, config
from collections import OrderedDict
import datetime


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=False)
    account_name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    rank_level = db.Column(db.Integer, db.ForeignKey('rank.rank_level'), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    rank = db.relationship('Rank', backref='account')

    def __init__(self, account_name, password_clear, domain, rank):
        self.account_name = account_name
        self.created = datetime.datetime.now()
        self.password = self.get_crypt_password(password_clear)
        self.rank = rank
        self.domain = domain

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return_dict = OrderedDict()

        return_dict['id'] = self.id
        return_dict['domain_id'] = self.domain_id
        return_dict['account_name'] = self.account_name

        return return_dict

    def get_crypt_password(self, password_clear):
        password_hash = hashlib.sha512((self.created.isoformat() +
                                        password_clear +
                                        config.PASSWORD_PEPPER).encode())

        return password_hash.hexdigest()

    def check_password(self, password_clear):
        password_hash = self.get_crypt_password(password_clear)

        return password_hash == self.password

    def is_domain_admin(self):
        return self.rank_level == 1