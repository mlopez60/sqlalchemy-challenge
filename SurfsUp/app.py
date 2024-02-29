# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

def startdate():
    session = Session(engine)

    # Get start date
    recent = session.query(Measurement.date).order_by((Measurement.date).desc()).first()
    enddate = dt.datetime.strptime(recent[0], "%Y-%m-%d")
    startdate = enddate - dt.timedelta(days=366)

    session.close()

    return(startdate)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Date/Precipitation data:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Dates and Temperature for the most active stations:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Temperature MIN, AVG, MAX data for specified start and/or range dates:<br/>"
        f"Insert start date in below link YYYY-MM-DD Format<br/>"
        f"/api/v1.0/<start><br/>"
        f"Insert start/end date in below link YYYY-MM-DD/YYYY-MM-DD Format<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation and dates"""

    # Query for data
    prcpdata = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > startdate()).all()

    session.close()

    # Store in dict
    prcpstore = []
    for date, prcp in prcpdata:
        prcpdict = {}
        prcpdict['date'] = date
        prcpdict['prcp'] = prcp
        prcpstore.append(prcpdict)
    
    return jsonify(prcpstore)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""

    # Query for data
    station = session.query(Station.station,).all()

    session.close()

    # Store in dict
    stationlist = list(np.ravel(station))
    
    return jsonify(stationlist)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp observations from previous year for most active station"""

    # Query for data
    tempdata = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-17').filter(Measurement.station == 'USC00519281').all()


    session.close()

    # Store in dict
    tempstore = []
    for date, tobs in tempdata:
        tempdict = {}
        tempdict['date'] = date
        tempdict['tobs'] = tobs
        tempstore.append(tempdict)
    
    return jsonify(tempstore)


@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, max temp for start date"""

    # Query for data
    startenddata = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()


    session.close()

    # Store in dict
    startendlist = []
    for min, avg, max in startenddata:
        startenddict = {}
        startenddict['min'] = min
        startenddict['avg'] = avg
        startenddict['max'] = max
        startendlist.append(startenddict)
    
    return jsonify(startendlist)


@app.route('/api/v1.0/<start>')
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, max temp for start date"""

    # Query for data
    startdata = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()


    session.close()

    # Store in dict
    startlist = []
    for min, avg, max in startdata:
        startdict = {}
        startdict['min'] = min
        startdict['avg'] = avg
        startdict['max'] = max
        startlist.append(startdict)
    
    return jsonify(startlist)


if __name__ == '__main__':
    app.run(debug=True)