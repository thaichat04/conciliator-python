import requests
import jwt as pyjwt
import base64

from conciliator.connector import Connector
from conciliator.entity import Entity
from conciliator.file import File
from conciliator.document import Document
from conciliator.page import Page
from conciliator.invoice import Invoice

API_VERSION =  "api/v0/"

app_url = "https://app.expert.conciliator.ai/"
api_url = app_url + API_VERSION
session = None

current_entity: Entity = None

def url(l):
    global app_url
    global api_url
    app_url = l
    api_url = l + API_VERSION

def connect(username, pwd, tenant=None):
    global session
    if not isinstance(session, requests.Session):
        session = requests.Session()
    params = {'callbackUrl': app_url + "?jwtResponse=${jwtResponse}"}
    r = session.get(api_url + "user/loginRedirectionUrl", params=params)

    jwt = r.text.split("=")[1]
    jwt_decoded = pyjwt.decode(jwt, verify=False)
    api_app_url = jwt_decoded["sub"]
    r = session.get(r.text)

    jwt = r.url.split("=")[1]
    credentials = base64.b64encode(("%s:%s" % (username, pwd)).encode()).decode("utf-8")
    payload = {'type': "basic", 'value': credentials, 'accountStore': {'href': api_app_url}}
    r = session.post(api_app_url + "/loginAttempts", json=payload,
                          headers={'Authorization': "Bearer %s" % jwt})
    r.raise_for_status()
    if r.text:
        # Tenant selection
        bearer = r.headers['authorization']
        org_url = r.json()['account']['href'] + '/organizations'
        r = session.get(org_url,
                             params = {'offset':0, 'limit': 10, 'q': tenant},
                             headers={'Authorization': "%s" % bearer})
        tenant_id = None
        for t in r.json()['items']:
            if t['nameKey'] == tenant:
                tenant_id = t['id']
                break
        if not tenant_id: raise ValueError('Cannot find tenant')
        bearer = r.headers['authorization']
        r = session.post(org_url + '/' + tenant_id,  headers={'Authorization': "%s" % bearer})

    jwt = r.headers['Stormpath-SSO-Redirect-Location'].split("=")[1]
    params = {'jwtResponse': jwt}
    session.get(api_url + "user/loginResult", params=params)
    return True

