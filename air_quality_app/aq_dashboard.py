'''
OpenAQ Air Quality Dashboard with Flask.
When you run a Python file directly (e.g., python app.py)
__name__ is set to "__main__"
When the file is imported as a module, __name__ is the module's name
(e.g., aq_dashboard for aq_dashboard.py)
'''
from flask import Flask, render_template, request, jsonify
from .air_quality import get_results
from .models import DB, Record

import warnings
warnings.filterwarnings("ignore")


def get_list_of_tuples():
    response = get_results()

    list_data = [(measurement['datetime']['utc'], measurement['value'])
                 for measurement in response['results']]

    return list_data


def create_app():
    '''
    Instantiate Flask class, initializing web application
    Pass current module name (app) to Flask class
    (tells Flask where to look for templates, static files, and other
    resources) which is the root path of the application
    '''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/', methods=['POST', 'GET'])
    def root():
        """Base view."""
        if request.method == "GET":
            with app.app_context():
                filtered_records = Record.query.filter(Record.value >= 10).all()
                return render_template('base.html', filtered_records=filtered_records, message='')
        elif request.method == "POST":
            location_name = request.values['location_name']
            location = 

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()

        records = get_list_of_tuples()

        for record in records:
            db_record = Record(datetime_utc=record[0],
                               value=record[1])
            DB.session.add(db_record)

        DB.session.commit()
        return root()

    return app
