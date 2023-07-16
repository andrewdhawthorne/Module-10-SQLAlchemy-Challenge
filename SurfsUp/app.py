# Import the dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement 
station = base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
# Create an app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value

    # Create the session 
    session = Session(engine)

   # Find the most recent date in the data set
    closest_date = session.query(func.max(measurement.date)).first()
    closest_date

    # Design a query to retrieve the last 12 months of precipitation data and plot the results 
    # starting from the most recent data point in the database 

    # Calculate the date one year from the last date in data set
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    one_year = session.query(measurement.date, measurement.prcp).filter(measurement.date >= first_date).all()

    # Close the session                   
    session.close()

    # Create a dictionary from the row data and append to a list of prcp_list
    prcp_list = []
    for date, prcp in one_year:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    # Return the JSON representation of your dictionary
    return jsonify(prcp_list)