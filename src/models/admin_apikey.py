from mailapi import db, config
from collections import OrderedDict
import datetime
import uuid


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
