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
