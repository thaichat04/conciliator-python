import json
import conciliator
from conciliator.entity import Entity
from conciliator.page import Page
from conciliator.document import Document
from conciliator.conciliatorobj import ConciliatorObj
import datetime

class File(ConciliatorObj):

    id: str
    name: str
    created: datetime.datetime
    status: str
    error: str
    user: str
    connector: str
    nb_pages: int
    entity_id: str


    @classmethod
    def list(cls, entity: Entity=None, nb=100, q=None):
        # TODO: next page with param 'last_id'
        if not entity: entity = conciliator.current_entity
        if not entity: raise ValueError('Entity is missing')
        params = {'entity_id': entity.id, 'limit': nb, 'q': q}
        r = conciliator.session.get(conciliator.api_url + "files", params=params)
        if r.status_code != 200:
            raise ValueError("Could not get file list")
        l = []
        for js in json.loads(r.text)['rowData']:
            js['entity_id'] = entity.id
            l.append(File(js))
        return l

    @classmethod
    def load(cls, entity: Entity=None, name: str=None):
        #FIXME: need to load by Id
        fs = File.list(entity, q=name)
        if len(fs) > 1: raise ValueError('Not unique result')
        if len(fs) == 0: return None
        return fs[0]

    def pages(self):
        r = conciliator.session.get(conciliator.api_url + "files/" + self.id + "/pages")
        if r.status_code != 200:
            raise ValueError("Could not get pages from file")
        l = []
        for js in json.loads(r.text):
            l.append(Page(js))
        return l

    def documents(self):
        # FIXME: need search by file_id and not filename
        params = {'entity_id': self.entity_id, 'file_name': self.name}
        r = conciliator.session.get(conciliator.api_url + 'documents/', params=params )
        l = []
        for js in json.loads(r.text)['rowData']:
            l.append(Document(js))
        return l