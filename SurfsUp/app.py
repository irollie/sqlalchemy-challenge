# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy *

import flask *


#################################################
# Database Setup
#################################################

#Create engine with the sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Create the base
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurements = Base.classes.measurements
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tob<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYY.</p>"

    )

        
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from the last date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query for the date and precipitaion for the last year
    precipitation = sesion.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    session.close()
    #
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)



@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Station.station).all()

    session.close()

    #convert results in an list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)



@app.route("/api/v1.0/tob")
def tob():
    """Return the temperature observations (tobs) for the previous year"""
    # Calculate the date 1 year ago from the last date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    session.close()

    #convert results in an list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX"""

    #select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date ,= end).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)



if __name__ == '__main__'
    app.run()