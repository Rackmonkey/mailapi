from mailapi import db


class Rank(db.Model):
    __tablename__ = 'rank'

    rank_level = db.Column(db.Integer, primary_key=True)
    rank_name = db.Column(db.String(), unique=True)

    def __init__(self, rank_level, rank_name):
        self.rank_level = rank_level
        self.rank_name = rank_name

    def __repr__(self):
        return '<id {}>'.format(self.id)
