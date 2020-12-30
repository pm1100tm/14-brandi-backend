

from flask.json import JSONEncoder
from flask import Flask
from flask_cors import CORS

from model import SampleUserDao, EventDao
from service import SampleUserService, EventService
from view import create_endpoints

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        import datetime
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat(sep=' ')
            if isinstance(obj, datetime.datetime):
                return obj.isoformat(sep=' ')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


# for getting multiple service classes
class Services:
    pass


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True

    app.json_encoder = CustomJSONEncoder
    # By default, submission of cookies across domains is disabled due to the security implications.
    CORS(app, resources={r'*': {'origins': '*'}})

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = app.config['DB']

    # persistence Layer
    sample_user_dao = SampleUserDao()
    event_dao = EventDao()

    # business Layer
    services = Services
    services.sample_user_service = SampleUserService(sample_user_dao)
    services.event_service = EventService(event_dao)

    # presentation Layer
    create_endpoints(app, services, database)

    return app
