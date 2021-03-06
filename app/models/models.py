from app import db
import json
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
                if "query" in fields:
                    del fields["query"]
                if "query_class" in fields:
                    del fields["query_class"]
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)


class AuthPermission(db.Model):
    __tablename__ = "auth_permission"
    id = db.Column(db.Integer, primary_key=True)
    content_type_id = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True)
    codename = db.Column(db.String(64), unique=True)

    def __init__(self, id, content_type_id, name, codename):
        self.id = id
        self.content_type_id = content_type_id
        self.name = name
        self.codename = codename


    def __repr__(self):
        return '<User %r>' % (self.codename)
