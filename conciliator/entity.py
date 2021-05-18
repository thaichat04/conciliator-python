import conciliator
import datetime
from conciliator.conciliatorobj import ConciliatorObj
import json

class Entity(ConciliatorObj):

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
        r = conciliator.session.get(conciliator.api_url + "entities", params=params)
        r.raise_for_status()
        for e in r.json():
            l.append(Entity(e))
        return l

    @classmethod
    def load(cls, query=None):
        es = Entity.list(query)
        if len(es) > 1: raise ValueError('Not unique result')
        if len(es) == 0: return None
        return es[0]

    def __str__(self):
        return self.identifier + ' - ' + self.name

    def set_current(self):
        conciliator.current_entity = self

    def save(self):
        r = conciliator.session.patch(conciliator.api_url + "entities",
                                       data=json.dumps([self.serialize(),]),
                                       headers={'Content-type': 'application/json'})
        r.raise_for_status()
        return True
