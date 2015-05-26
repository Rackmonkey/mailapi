import hashlib
from mailapi import db, config
from collections import OrderedDict
import datetime
import uuid
# from sqlalchemy.dialects.postgresql import JSON


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


class AdminApikey(db.Model):
    __tablename__ = 'admin_apikey'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    apikey = db.Column(db.String(), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(), nullable=True)

    def __init__(self, admin_id,  description=None):
        self.admin_id = admin_id
        self.apikey = str(uuid.uuid1())
        self.description = description
        self.created = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return_dict = OrderedDict()

        return_dict['id'] = self.id
        return_dict['admin_id'] = self.admin_id
        return_dict['apikey'] = self.apikey
        return_dict['description'] = self.description
        return_dict['created'] = self.created

        return return_dict


class Domain(db.Model):
    __tablename__ = 'domain'

    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(), unique=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    accounts = db.relationship('Account', backref='domain')
    aliases = db.relationship('Alias', backref='domain')

    def __init__(self, domain_name, admin):
        self.domain_name = domain_name
        self.admin = admin
        self.created = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return_dict = OrderedDict()

        return_dict['id'] = self.id
        return_dict['domain_name'] = self.domain_name

        return return_dict


class Alias(db.Model):
    __tablename__ = 'alias'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=False)
    source = db.Column(db.String(), nullable=False)
    destination = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, domain, source, destination):
        self.domain = domain
        self.source = source
        self.destination = destination

        self.created = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return_dict = OrderedDict()

        return_dict['id'] = self.id
        return_dict['username'] = self.username

        return return_dict


class Rank(db.Model):
    __tablename__ = 'rank'

    rank_level = db.Column(db.Integer, primary_key=True)
    rank_name = db.Column(db.String(), unique=True)

    def __init__(self, rank_level, rank_name):
        self.rank_level = rank_level
        self.rank_name = rank_name

    def __repr__(self):
        return '<id {}>'.format(self.id)


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