import json
import conciliator
import datetime
from json import JSONEncoder

# TODO: a mettre dans utils
# Credits: https://gist.github.com/abhinav-upadhyay/5300137
class DateTimeEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return datetime.datetime.strftime(obj, '%Y-%m-%d')
        else:
            return JSONEncoder.default(self, obj)

class Entity:

    id: str
    code: str                   # code APE
    code_description: str       # description APE
    fisc_start: datetime.date
    fisc_end: datetime.date
    identifier: str
    name: str
    siret: str

    @classmethod
    def list(cls, query=None):
        l = []
        params = {'q': query}
        for js in json.loads(conciliator.session.get(conciliator.api_url + "entities", params=params).text):
            l.append(Entity(js))
        return l

    def __init__(self, data):
        # remove deprecated
        data.pop('activity', None)
        data.pop('type_activity', None)
        # convert types
        if data['fisc_start']: data['fisc_start'] = datetime.datetime.strptime(data['fisc_start'], '%Y-%m-%d').date()
        if data['fisc_end']  : data['fisc_end']   = datetime.datetime.strptime(data['fisc_end'],   '%Y-%m-%d').date()
        self.__dict__ = data

    def __str__(self):
        return self.identifier + ' - ' + self.name

    def save(self):
        r = conciliator.session.patch(conciliator.api_url + "entities",
                                      data=json.dumps([self.__dict__,], cls=DateTimeEncoder),
                                      headers={'Content-type': 'application/json'})
        if r.status_code != 204:
            raise ValueError("Cannot save entity")
        return True