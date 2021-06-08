"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
import os
from flask import request, redirect, render_template, url_for
import arrow
import acp_times  # Brevet time calculations
import config
import insertion_retrieval
from pymongo import MongoClient

import logging

###
# Globals
###
app = flask.Flask(__name__)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

CONFIG = config.configuration()
#app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    app.logger.debug("request.args: {}".format(request.args))
    km = request.args.get('km', 999, type=float)
    start = request.args.get('start', type=str)  # get date
    brevet_dist = request.args.get('brevet_dist', type=int)
    start = arrow.get(start, 'YYYY-MM-DDTHH:mm')  # convert to arrow
    app.logger.debug("km={}".format(km))

    open_time = acp_times.open_time(km, brevet_dist, start).format('YYYY-MM-DDTHH:mm')  # pass with correct start time
    close_time = acp_times.close_time(km, brevet_dist, start).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_display", methods=['POST'])
def _display():
    entries = insertion_retrieval.retrieval(db)
    if entries.count() == 0:
        return render_template("submissionError.html")
    return render_template("display.html", entries=entries)

@app.route("/_submit", methods=['POST'])
def _submit():
    kmList = request.form.getlist("km")  # get all of the items for key
    kmList = [i for i in kmList if i]  # filter out "" 
    openList = request.form.getlist("open")
    openList = [i for i in openList if i]
    closeList = request.form.getlist("close")
    closeList = [i for i in closeList if i]
    if len(kmList) == len(openList) == len(closeList) != 0:
        insertion_retrieval.insert(db, kmList, openList, closeList)
    elif len(kmList) == 0:
        # problem print error
        app.logger.debug("Error: length 0")
        return render_template("submissionError.html")
    else: 
        app.logger.debug("Internal Error")
        return render_template("submissionError.html")
    # result = {"message": "Success"}
    return redirect(url_for("index"))
        

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
