import json
import conciliator
import datetime

class Connector:
    name: str
    id: str
    category: object # TODO
    config: object   # TODO
    lastExecution: datetime.datetime # '2020-09-29T07:48:19.645888Z'
    linkExports: object
    numberInProcess: int
    numberLoaded: int
    numberRejected: int
    pause: bool
    status: str
    warning: object

    @classmethod
    def list(cls):
        connectors = []
        for js in json.loads(conciliator.session.get(conciliator.api_url + "connectors").text):
            connectors.append(Connector(js))
        return connectors

    def __init__(self, data):
        # convert types
        if data['lastExecution']:
            data['lastExecution'] = datetime.datetime.fromisoformat(data['lastExecution'].replace('Z', '+00:00'))
        self.__dict__ = data

    def logs(self, nb=100):
        params = {'nbItems': nb}
        j = json.loads(
            conciliator.session.get(conciliator.api_url + "connectors/" + self.id + "/logs", params=params).text)
        return j
