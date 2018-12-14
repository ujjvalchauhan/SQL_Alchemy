# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app
app = Flask(__name__)


import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).all()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for p in results:
        precipitation_dict = {}
        precipitation_dict["date"] = p.date
        precipitation_dict["tobs"] = p.tobs
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    # query all stations
    results = session.query(Measurement.station).all()
    
     # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).all()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):

    
    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    tobs=[]
    for row in result:
        tobs_dict = {}
        tobs_dict["TMIN"] = row[0]
        tobs_dict["TAVG"] = row[1]
        tobs_dict["TMAX"] = row[2]
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps_dates(start_date, end_date):

    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    
    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    tobs=[]
    for row in result:
        tobs_dict = {}
        tobs_dict["TMIN"] = row[0]
        tobs_dict["TAVG"] = row[1]
        tobs_dict["TMAX"] = row[2]
        tobs.append(tobs_dict)

    return jsonify(tobs)
    

if __name__ == '__main__':
    app.run(debug=True)

 