import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from flask import (
    Flask,
    render_template,
    jsonify,
    request)


engine=create_engine("sqlite:///belly_button_biodiversity.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
inspector = inspect(engine)

otu=Base.classes.otu
samples=Base.classes.samples
metadata=Base.classes.samples_metadata

session=Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/names")
def get_names():
    sample_cols=inspector.get_columns("samples")
    sample_names=[col["name"] for col in sample_cols ]
    return jsonify(sample_names)


@app.route("/otu")
def get_descript():
    otu_descript = session.query(otu.lowest_taxonomic_unit_found).all()
    otus = list(np.ravel(otu_descript))
    return jsonify(otus)

@app.route("/metadata/<sample>")
def get_metadata(sample):
    sample=sample.split("_")[1]
    meta_query=session.query(metadata.AGE,metadata.BBTYPE,metadata.ETHNICITY,metadata.GENDER,metadata.LOCATION,metadata.SAMPLEID).filter(metadata.SAMPLEID==sample).all()
    meta_dict_response={"age":meta_query[0][0],"bbtype":meta_query[0][1],"ethnicity":meta_query[0][2],"gender":meta_query[0][3],"location":meta_query[0][4],"sampleid":meta_query[0][5]}
    return jsonify(meta_dict_response)
# get metadata for a given sample "BB_940" get age, bbtype, ethnicity, gender, location, sampleid

@app.route("/wfreq/<sample>")
def get_wfreq(sample):
    sample=sample.split("_")[1]
    wfreq_query=session.query(metadata.WFREQ).filter(metadata.SAMPLEID==sample).all()    
    wfreq = np.ravel(wfreq_query)[0]
    return jsonify(wfreq)
# go to samples_metadata table, return wfreq column that matches given sample

@app.route("/samples/<sample_name>")
def get_dict(sample_name):
    lookup_value="samples.{}".format(sample_name)
    sample_data=session.query(samples.otu_id,lookup_value).all()
    sample_df=pd.DataFrame({"otu_id":[],"sample_values":[]})
    for index in range(len(sample_data)):
        sample_df.at[index,"otu_id"]=sample_data[index][0]
        sample_df.at[index,"sample_values"]=sample_data[index][1]
        sample_df=sample_df.sort_values(by='sample_values',ascending=False)
        sample_df_10=sample_df.head(10)
        sample_dict=sample_df_10.to_dict(orient="list")
    return jsonify(sample_dict)



if __name__ == "__main__":
    app.run(debug=True)