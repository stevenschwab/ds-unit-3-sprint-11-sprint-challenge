'''
OpenAQ Air Quality Dashboard with Flask.
When you run a Python file directly (e.g., python app.py)
__name__ is set to "__main__"
When the file is imported as a module, __name__ is the module's name
(e.g., aq_dashboard for aq_dashboard.py)
'''
from flask import Flask, render_template, request, redirect, url_for
from .air_quality import get_results, get_measurements_by_location
from .models import DB, Location, Record
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

import warnings
warnings.filterwarnings("ignore")


def get_list_of_tuples():
    response = get_results()

    list_data = [(measurement['datetime']['utc'], measurement['value'])
                 for measurement in response['results']]

    return list_data


def get_analysis_data():
    """Compute averages, trends, and a prediction."""
    # Averages by location
    averages = DB.session.query(
        Location.name,
        DB.func.avg(Record.value).label('avg_value')
    ).join(Record).group_by(Location.id).all()

    # Trends (average value per day)
    trends = DB.session.query(
        DB.func.date(Record.datetime_utc).label('date'),
        DB.func.avg(Record.value).label('avg_value')
    ).group_by(DB.func.date(Record.datetime_utc)).order_by('date').all()

    # Linear regression for prediction
    records = Record.query.all()
    if records:
        df = pd.DataFrame([
            {'date': r.datetime_utc, 'value': r.value}
            for r in records
        ])
        df['date_ordinal'] = df['date'].map(lambda x: x.toordinal())
        model = LinearRegression()
        model.fit(df[['date_ordinal']], df['value'])
        next_day = (datetime.now(datetime.timezone.utc) + timedelta(days=1)).toordinal()
        prediction = model.predict([[next_day]])[0]
    else:
        prediction = 0.0
    
    return averages, trends, prediction


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
        """Base view with location search."""
        with app.app_context():
            DB.create_all()  # Ensure tables exist
            if request.method == "POST":
                location_name = request.values['location_name']
                if not location_name:
                    return render_template('base.html', filtered_records=[], message='Location name is required')

                # Fetch OpenAQ data
                try:
                    response = get_measurements_by_location(location_name)
                    # Get or create location
                    location = Location.query.filter_by(name=location_name).first()
                    if not location:
                        location = Location(name=location_name, country=response['results'][0].get
                                            ('country', 'Unknown') if response['results'] else 'Unknown')
                        DB.session.add(location)
                        DB.session.commit()

                    # Add new records
                    for m in response['results']:
                        datetime_utc = pd.to_datetime(m['datetime']['utc'], format='mixed')
                        # Check if record exists
                        if not Record.query.filter_by(location_id=location.id,
                                                      datetime_utc=datetime_utc).first():
                            record = Record(
                                location_id=location.id,
                                datetime_utc=datetime_utc,
                                value=m['value']
                            )
                            DB.session.add(record)
                    DB.session.commit()
                except Exception as e:
                    return render_template('base.html', filtered_records=[], message=f"API error: {str(e)}")

            filtered_records = Record.query.filter(Record.value >= 10).all()
            averages, trends, prediction = get_analysis_data()
            return render_template('base.html', filtered_records=filtered_records, message='',
                                   averages=averages, trends=trends, prediction=prediction)

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ without dropping existing data."""
        try:
            response = get_results()  # Fetch general measurements
            for m in response['results']:
                location_name = m.get('location', 'Unknown')
                location = Location.query.filter_by(name=location_name).first()
                if not location:
                    location = Location(name=location_name, country=m.get('country', 'Unknown'))
                    DB.session.add(location)
                    DB.session.commit()

                datetime_utc = pd.to_datetime(m['datetime']['utc'], format='mixed')
                if not Record.query.filter_by(location_id=location.id, datetime_utc=datetime_utc).first():
                    record = Record(
                        location_id=location.id,
                        datetime_utc=datetime_utc,
                        value=m['value']
                    )
                    DB.session.add(record)
            DB.session.commit()
            return redirect(url_for('root'))
        except Exception as e:
            return render_template('base.html', filtered_records=[], message=f"API error: {str(e)}")

    return app
