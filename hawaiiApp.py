import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitaton"""
    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs"""
    # Query all precipitation
    results = session.query(measurement.station, measurement.date, measurement.prcp).\
        filter(measurement.station =="USC00519281").\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.date <= '2017-08-23').order_by(measurement.date).all()

    session.close()
    
    # Convert list of tuples into normal list
    all_tobs = []
    for station, date, prcp in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def get_t_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of functions """
    # Query all 
    results = session.query(measurement.date, func.avg(measurement.tobs), func.max(measurement.tobs),func.min(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    all_start = []
    for date, avg, max, min in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["avg"] = avg
        start_dict["max"] = max
        start_dict["min"] = min
        all_start.append(start_dict)

    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<stop>")
def get_t_start_stop(start,stop):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of functions """
    # Query all 
    results = session.query(measurement.date, func.avg(measurement.tobs), func.max(measurement.tobs),func.min(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= stop).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    all_stop = []
    for date, avg, max, min in results:
        stop_dict = {}
        stop_dict["date"] = date
        stop_dict["avg"] = avg
        stop_dict["max"] = max
        stop_dict["min"] = min
        all_stop.append(stop_dict)

    return jsonify(all_stop)



if __name__ == '__main__':
    app.run(debug=True)
