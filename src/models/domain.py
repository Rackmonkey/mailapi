from mailapi import db
from collections import OrderedDict
import datetime


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