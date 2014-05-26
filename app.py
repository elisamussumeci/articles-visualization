from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import cPickle as CP
import datetime
import json
import zlib

import dateutil.parser
import pymongo
import pysolr

from bson import json_util, ObjectId

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.errorhandler(500)
def page_not_found(e):
    return e, 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)