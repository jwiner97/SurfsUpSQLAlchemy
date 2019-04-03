import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
        f"/api/v1.0/tobs</br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation level for date within last 12 months"""
    # Query precipitation
    results = engine.execute('''select date(m.date), prcp
    from measurement m
    inner join station s on s.station = m.station
    where m.date >= date('2016-08-23')
    order by m.date
''').fetchall()

    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    precipitation = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query staions
    results = engine.execute('''select m.station,s.name,s.latitude,s.longitude,s.elevation, count(m.station) as count
from measurement m
inner join station s on s.station = m.station
group by m.station''').fetchall()

    # Convert the query results to a Dictionary
    stations = []
    for station,name,latitude,longitude,elevation,count in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_dict["count"] = count
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def stations():
    """Return a JSON list of Temperature Observations (tobs) for the previous year.."""
    # Query staions
    results = engine.execute('''select m.station,s.name,s.latitude,s.longitude,s.elevation, count(m.station) as count
from measurement m
inner join station s on s.station = m.station
group by m.station''').fetchall()

    # Convert the query results to a Dictionary
    stations = []
    for station,name,latitude,longitude,elevation,count in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_dict["count"] = count
        stations.append(station_dict)

    return jsonify(stations)





if __name__ == '__main__':
    app.run(debug=True)
