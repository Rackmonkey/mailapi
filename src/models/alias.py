from mailapi import db, config
from collections import OrderedDict
import datetime


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
