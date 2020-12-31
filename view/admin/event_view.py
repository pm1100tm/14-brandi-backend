import json
from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail, DateMissingOne, EventSearchTwoInput, FilterDoesNotMatch

from utils.rules import NumberRule, EventStatusRule, EventExposureRule, DateRule, ProductMenuRule, CategoryFilterRule
from flask_request_validator import (
    Param,
    JSON,
    GET,
    validate_params
)

def date_converter(o):
    import datetime
    if isinstance(o, datetime.datetime):
        return o.__str__()

class EventView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('name', GET, str, required=False),
        Param('number', GET, str, required=False, rules=[NumberRule()]),
        Param('status', GET, str, required=False, rules=[EventStatusRule()]),
        Param('exposure', GET, int, required=False, rules=[EventExposureRule()]),
        Param('page', GET, int, required=True),
        Param('length', GET, int, required=True),
        Param('start_date', JSON, str, required=False, rules=[DateRule()]),
        Param('end_date', JSON, str, required=False, rules=[DateRule()])
    )
    def get(self, *args):
        data = {
            'name': args[0],
            'number': args[1],
            'status': args[2],
            'exposure': args[3],
            'page': args[4],
            'length': args[5],
            'start_date': args[6],
            'end_date': args[7]
        }
        if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
            raise DateMissingOne('start_date or end_date is missing')

        if data['name'] and data['number']:
            raise EventSearchTwoInput('search value accept only one of name or number')

        try:
            connection = get_connection(self.database)
            events = self.service.get_events_service(connection, data)
            return jsonify({'message': 'success', 'result': events})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventProductsCategoryView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('filter', JSON, str, required=True, rules=[CategoryFilterRule()]),
        Param('menu_id', JSON, int, required=False, rules=[ProductMenuRule()]),
        Param('first_category_id', JSON, int, required=False)
    )
    def get(self, *args):
        data = {
            'filter': args[0],
            'menu_id': args[1],
            'first_category_id': args[2]
        }
        if data['filter'] is "none" and (data['menu_id'] or data['first_category_id']):
            raise FilterDoesNotMatch('error: filter does not match')
        elif data['filter'] == "menu":
            if not data['menu_id']:
                raise FilterDoesNotMatch('error: filter does not match')
            if data['first_category_id']:
                raise FilterDoesNotMatch('error: filter does not match')
        elif data['filter'] == "both":
            if not data['menu_id'] or not data['first_category_id']:
                raise FilterDoesNotMatch('error: filter does not match')

        try:
            connection = get_connection(self.database)
            result = self.service.get_products_category_service(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
