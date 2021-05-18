import conciliator
import datetime
from conciliator.conciliatorobj import ConciliatorObj

class Connector(ConciliatorObj):
    name: str
    id: str
    category: object
    config: object
    lastExecution: datetime.datetime
    linkExports: object
    numberInProcess: int
    numberLoaded: int
    numberRejected: int
    pause: bool
    status: str
    warning: object
    type: str

    def __init__(self, data):
        super().__init__(data)
        self.type = self.category['id']

    @classmethod
    def list(cls):
        connectors = []
        r = conciliator.session.get(conciliator.api_url + "connectors")
        r.raise_for_status()
        for js in r.json():
            connectors.append(Connector(js))
        return connectors

    def param(self, name):
        for conf in self.config:
            if conf['name'] == name:
                return conf['value']
        raise ValueError("Config parameter not found")

    def logs(self, nb=100):
        params = {'nbItems': nb}
        r = conciliator.session.get(conciliator.api_url + "connectors/" + self.id + "/logs", params=params)
        r.raise_for_status()
        # TODO
        return r.json()

    # zip files
    # GET 200 OK
    # https://app.expert.conciliator.ai/api/v0/connectors/8f41b5f4-1700-4334-a21d-a197fc852b84?baseUrl=https://app.expert.conciliator.ai&connectorPageUrl=https://app.expert.conciliator.ai/connectors/8f41b5f4-1700-4334-a21d-a197fc852b84
    # params: baseUrl=https://app.expert.conciliator.ai&connectorPageUrl=https://app.expert.conciliator.ai/connectors/8f41b5f4-1700-4334-a21d-a197fc852b84
    # Response:
    # "linkExports":[
    #       {
    #          "id":"1eb29a0a-2607-ca30-95a5-d062d3327d02",
    #          "name":"conciliator-isacompta-2020-11-18-14-19-06.zip",
    #          "baseURL":"https://app.expert.conciliator.ai/api/v0/connectors/8f41b5f4-1700-4334-a21d-a197fc852b84/download/1eb29a0a-2607-ca30-95a5-d062d3327d02",
    #          "downloaded":false
    #
    # Download
    # GET 200 OK
    # https://app.expert.conciliator.ai/api/v0/connectors/8f41b5f4-1700-4334-a21d-a197fc852b84/download/1eb29a0a-2607-ca30-95a5-d062d3327d02