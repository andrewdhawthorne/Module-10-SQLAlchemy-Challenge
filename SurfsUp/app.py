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

# Reflect an existing database into a new model
base = automap_base()

# Feflect the tables
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
#   to a dictionary using date as the key and prcp as the value

    # Create the session 
    session = Session(engine)

   # Find the most recent date in the data set
    closest_date = session.query(func.max(measurement.date)).first()
    closest_date

    # Design a query to retrieve the last 12 months of precipitation data and plot the results 
    #   starting from the most recent data point in the database 

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

@app.route("/api/v1.0/stations")
def stations(): 
 # Create the session 
    session = Session(engine)

    # Design a query to calculate the total number of stations in the dataset
    total_stations = session.query(func.count(station.station)).first()

     # Close the session                   
    session.close()

    # Return a JSON list of stations from the dataset
    return jsonify(total_stations)

@app.route("/api/v1.0/tobs")
def tobs(): 
# Query the dates and temperature observations of the most-active station for the previous year of data

    # Create the session 
    session = Session(engine)

    # Calculate the date one year from the last date in data set
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    # List the stations and their counts in descending order
    most_active_stations = session.query(measurement.station, func.count(measurement.station)).\
                    group_by(measurement.station).\
                    order_by(func.count(measurement.station).desc()).all()
    most_active_stations

    # Using the most active station id query the last 12 months of temperature observation data for this station
    twelve_mo = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= first_date).all()
    
    # Close the session                   
    session.close()

    # Return a JSON list of temperature observations for the previous year
    return jsonify(twelve_mo)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None): 
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range 

# Create the session 
    session = Session(engine)

    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    # Query for the minimun, average, and maxium temperature 
    sel=[func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    # Use if/else statement to loop through data from start date to most recent date 
    if end == None:
        specific_start = session.query(*sel).\
            filter(measurement.date >= start).all()
        
        # Returns list of tuples, which need to be converted into a regular list 
        specific_start_list = list(np.ravel(specific_start)) 
        
        # Return a JSON list of TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
        return jsonify(specific_start_list)

    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive        
    else: 
       specific_end = session.query(*sel).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()

    # Return a JSON list of temperature observations for the previous year
    return jsonify(specific_end)

# Close the session
session.close()

# Define main branch 
if __name__ == "__main__":
    app.run(debug = True)