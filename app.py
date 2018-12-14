
from flask import Flask, jsonify

app = Flask(__name__)


import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

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

    all_precipitations = []
    for p in results:
        precipitation_dict = {}
        precipitation_dict["date"] = p.date
        precipitation_dict["tobs"] = p.tobs
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Measurement.station).all()
 
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

 
