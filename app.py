#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
    #return 'Hello world'

#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#import sql dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask dependencies
from flask import Flask, jsonify

#Set Up the Database - access and query sqlite database
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect database into classes
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#save references for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link
session = Session(engine)

#create flask app - "app"
app = Flask(__name__)

#define welcome root, use f string to display data
#When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. This convention signifies that this is version 1 of our application
#@app.route("/")
#def welcome():
    #return(
    #'''
    #Welcome to the Climate Analysis API!.\
    #Available Routes:.\
    #/api/v1.0/precipitation.\
    #/api/v1.0/stations.\
    #/api/v1.0/tobs.\
    #/api/v1.0/temp/start/end.\
    #''')

#run flask in the command line

##precipitation route - query for percipitation
#@app.route("/api/v1.0/precipitation")
#def precipitation():
#prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#precipitation = session.query(Measurement.date, Measurement.prcp).\
    #filter(Measurement.date >= prev_year).all()
#return

#jsonify data
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#http://127.0.0.1:5000/ -> add "api/v1.0/precipitation" to see data

#stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#temp route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#statistics route - add start and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
