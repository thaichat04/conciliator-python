import conciliator as cc
from tests.mocksession import RecordSession
import json
from requests import HTTPError

config_file = 'password.json'

# config = {
#     #no tenant selection user
#     'onetenant': { 'username': 'foo', 'password': 'bar'},
#
#     #tenant selection
#     'selecttenant': { 'username': 'foo', 'password': 'bar', 'selectedtenant': 'Dhatim SAS', 'mutipletenants': 'ten'}
# }


config = json.load(open(config_file, 'r'))

## Record authentication

def record_authentication():

    cc.session = RecordSession()
    cc.session.storepath = 'data/auth_badlogin'
    try:
        cc.connect(config['onetenant']['username'], 'azerty')
    except HTTPError:
        print("bad login")

    cc.session = RecordSession()
    cc.session.storepath = 'data/auth_onetenant/'
    cc.connect(config['onetenant']['username'], config['onetenant']['password'])

    cc.session = RecordSession()
    cc.session.storepath = 'data/auth_selectedtenant'
    cc.connect(config['selecttenant']['username'], config['selecttenant']['password'], config['selecttenant']['selectedtenant'])


    cc.session = RecordSession()
    cc.session.storepath = 'data/auth_multipletenant'
    try:
        cc.connect(config['selecttenant']['username'], config['selecttenant']['password'], config['selecttenant']['mutipletenants'])
    except ValueError:
        print("cannot select tenant")


## Record data

def purge_data():
    pass

def record_data():
    cc.session = RecordSession()
    cc.session.storepath = 'data/junk'
    cc.connect(config['selecttenant']['username'], config['selecttenant']['password'],
               config['selecttenant']['selectedtenant'])
    cc.session.storepath = 'data/entities'
    cc.Entity.list()
    cc.session.storepath = 'data'
    e = cc.Entity.list('DH')[0]
    cc.current_entity = e
    #cc.session.storepath = 'data/files'
    # filename: Scannable Document on 4 Nov 2020 at 10_57_32.pdf

    cons = cc.Connector.list()

#record_authentication()
record_data()