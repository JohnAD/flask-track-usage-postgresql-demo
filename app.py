#
#  example Flask app that uses flask-track-usage and PostgreSQL
#
import os
from flask import (
    Flask,
    render_template,
    g
)
from flask_sqlalchemy import SQLAlchemy
from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage
# from flask_track_usage.summarization import sumUrl, sumUserAgent

#########################
#
#  SETUP FLASK and JINJA2
#
#########################
app = Flask(__name__)

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)
app.jinja_env.filters['datetime'] = datetimeformat

#########################
#
#  SETUP POSTGRESQL
#
#########################

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://temp:temp@localhost/track_usage_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sql_db = SQLAlchemy(app)

#########################
#
#  SETUP FLASK_TRACK_USAGE
#
#########################

FREEGEOIP_API_KEY = os.environ.get("FREEGEOIP_API_KEY", "NOT_SET")
app.config['TRACK_USAGE_USE_FREEGEOIP'] = True
app.config['TRACK_USAGE_FREEGEOIP_ENDPOINT'] = \
    "http://api.ipstack.com/{ip}" + \
    "?access_key={key}&fields=country_code".format(key=FREEGEOIP_API_KEY)
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'exclude'

traffic_storage = SQLStorage(db=sql_db, table_name="my_usage")
t = TrackUsage(app, traffic_storage)
# traffic_storage = SQLStorage(hooks=[sumUrl, sumUserAgent])
# t = TrackUsage(app, [traffic_storage])

#########################
#
#  PUBLIC ROUTES
#
#########################

@app.route('/')
def index():
#    g.track_var["something"] = 99
    return render_template('index.html')

@app.route('/page1')
def page_one():
#    g.track_var["something"] = 34
    return render_template('other_page.html', page_number=1)

@app.route('/page2')
def page_two():
    return render_template('other_page.html', page_number=2)

##########################
#
#  ADMIN ROUTES
#
##########################

@t.exclude
@app.route('/admin/last20.html')
def last_twenty():
    visits = traffic_storage.get_usage(limit=20)
    return render_template('last20.html', visits=visits)

@t.exclude
@app.route('/admin/last_url.html')
def last_url():
    stats = traffic_storage.get_sum(sumUrl, limit=30, target="http://127.0.0.1:5000/page1")
    return render_template('last_url.html', stats=stats)

@t.exclude
@app.route('/admin/last_useragent.html')
def last_useragent():
    stats = traffic_storage.get_sum(sumUserAgent, limit=40)
    return render_template('last_useragent.html', stats=stats)
