# shut up useless SA warning:
import warnings; warnings.filterwarnings('ignore', 'Unicode type received non-unicode bind param value.')
import logging

logging.basicConfig(level=logging.INFO)

from solr import SolrConnection

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_flatpages import FlatPages
from flaskext.mail import Mail

from offenesparlament import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('PARLAMENT_SETTINGS', silent=True)

db = SQLAlchemy(app)
pages = FlatPages(app)
mail = Mail(app)
_nkp = None


def solr():
    return SolrConnection(app.config['SOLR_URL'],
                http_user=app.config.get('SOLR_USER'),
                http_pass=app.config.get('SOLR_PASSWORD'))


def master_data():
    from webstore.client import URL as WebStore
    db, _ = WebStore(app.config['MASTER_URL'])
    return db

def etl_engine():
    from sqlaload import connect
    return connect(app.config['ETL_URL'])

def nk_persons():
    from nkclient import NKDataset
    global _nkp
    if _nkp is None:
        _nkp = NKDataset(app.config['NOMENKLATURA_PERSONS_DATASET'],
                     api_key=app.config['NOMENKLATURA_API_KEY'])
    return _nkp
