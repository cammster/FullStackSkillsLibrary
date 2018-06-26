#############################################################################################
#Step 4: Climate App
# 
#############################################################################################
from flask import Flask, jsonify

from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from collections import OrderedDict

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#############################################################################################
# Database Setup: select database, reflect database and table into a new model
############################################################################################
engine=create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

station=Base.classes.stations
measurement=Base.classes.measurements

session=Session(engine)

#############################################################################################
# Flask Setup
#############################################################################################
app=Flask(__name__)

#############################################################################################
# Created welcome page showing all available routes
#############################################################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

#############################################################################################
# Created route to show date and precipitation observations for last year of available data
#############################################################################################
@app.route("/api/v1.0/precipitation")
def last_year_prcp():
    """Return date and precipitation observations for most recent 12 months available data"""
    #Get most recent date available from database and go back 12 months
    most_recent=session.query(measurement.date).order_by(measurement.date.desc()).first()
    start_search=most_recent[0]-timedelta(days=365)
    #Query database for date and temp for last 12 months
    temp_prcp_result=session.query(measurement.date,measurement.prcp)\
        .filter(measurement.date>start_search).all()
    #Convert query results to dictionary using date:tobs
    temp_prcp_dict={}
    for i in range(len(temp_prcp_result)):
        temp_prcp_dict[datetime.strftime(temp_prcp_result[i][0],"%m-%d-%Y")]\
        =float(temp_prcp_result[i][1])
    #Return json representation of dictionary
    return jsonify(temp_prcp_dict)


############################################################################################
# Created route to return a json list of stations
#############################################################################################
@app.route("/api/v1.0/station")
def get_stations():
    station_list=session.query(station.name).all()
    station_list=list(np.ravel(station_list))
    station_list=[str(item) for item in station_list]
    return jsonify(station_list)

#############################################################################################
# Create route to return a json list of Temperature Observations for the last year
#############################################################################################
@app.route("/api/v1.0/tobs")
def last_year_tobs():
    """Return temperature observations for most recent 12 months available data"""
    #Get most recent date available from database and go back 12 months
    most_recent=session.query(measurement.date).order_by(measurement.date.desc()).first()
    start_search=most_recent[0]-timedelta(days=365)
    #Query database for date and temp for last 12 months
    temptobs_result=session.query(measurement.tobs)\
        .filter(measurement.date>start_search).all()
    temptobs_result=list(np.ravel(temptobs_result))
    temptobs_result=[float(item) for item in temptobs_result]
    #Return json response
    return jsonify(temptobs_result)

#############################################################################################
# Created route to return daily normals for date inputs
#############################################################################################
@app.route("/api/v1.0/<start_date>")
# def daily_trip_norm(start_date):
#     start=(datetime.strptime(str(start_date),"%Y-%m-%d")-timedelta(days=365)).strftime("%Y-%m-%d")
#     a_trip_norm=session.query(measurement.date,func.min(measurement.tobs),\
#             func.avg(measurement.tobs),func.max(measurement.tobs))\
#             .filter(func.strftime("%Y-%m-%d",measurement.date) >start)\
#             .group_by(measurement.date).all()
#     a_trip_norm_df=pd.DataFrame(OrderedDict({"Date":[],"Min_Temp":[],"Avg_Temp":[],"Max_Temp":[]}))
#     for index in range(len(trip_norm)):
#         a_trip_norm_df.at[index,"Date"]=a_trip_norm[index][0]
#         a_trip_norm_df.at[index,"Min_Temp"]=a_trip_norm[index][1]
#         a_trip_norm_df.at[index,"Avg_Temp"]=a_trip_norm[index][2]
#         a_trip_norm_df.at[index,"Max_Temp"]=a_trip_norm[index][3]
#     a_trip_norm_dict=a_trip_norm_df.to_dict(orient="records")

#     return jsonify(a_trip_norm_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def daily_trip_norm(start_date,end_date):
    """Return daily normals for trip duration based on start and end date,
     date format should be in MM-DD-YYYY """

    
    start=(datetime.strptime(str(start_date),"%Y-%m-%d")-timedelta(days=365)).strftime("%Y-%m-%d")
    end=(datetime.strptime(str(end_date),"%Y-%m-%d")-timedelta(days=365)).strftime("%Y-%m-%d")
    trip_norm=session.query(measurement.date,func.min(measurement.tobs),\
    func.avg(measurement.tobs),func.max(measurement.tobs))\
            .filter(func.strftime("%Y-%m-%d",measurement.date) >start\
            ,func.strftime("%Y-%m-%d",measurement.date)< end)\
            .group_by(measurement.date).all()

    trip_norm_df=pd.DataFrame(OrderedDict({"Date":[],"Min_Temp":[],"Avg_Temp":[],"Max_Temp":[]}))
    for index in range(len(trip_norm)):
        trip_norm_df.at[index,"Date"]=trip_norm[index][0]
        trip_norm_df.at[index,"Min_Temp"]=trip_norm[index][1]
        trip_norm_df.at[index,"Avg_Temp"]=trip_norm[index][2]
        trip_norm_df.at[index,"Max_Temp"]=trip_norm[index][3]
    trip_norm_dict=trip_norm_df.to_dict(orient="records")

    return jsonify(trip_norm_dict)

if __name__ == '__main__':
    app.run(debug=True)