import json
import conciliator
from conciliator.entity import Entity
from conciliator.page import Page
import datetime


class File:

    id: str
    name: str
    created: datetime.datetime
    status: str
    error: str
    user: str
    connector: str
    nb_pages: int
    thumbnail_page_number: int
    thumbnail_digest: str

    def __init__(self, data):
        # convert types
        if data['created']: data['created'] = datetime.datetime.fromisoformat(data['created'])
        self.__dict__ = data

    @classmethod
    def list(cls, entity: Entity, nb=100):
        # TODO: next page with param 'last_id'
        params = {'entity_id': entity.id, 'limit': nb}
        r = conciliator.session.get(conciliator.api_url + "files", params=params)
        if r.status_code != 200:
            raise ValueError("Could not get file list")
        l = []
        for js in json.loads(r.text)['rowData']:
            l.append(File(js))
        return l

    def pages(self):
        r = conciliator.session.get(conciliator.api_url + "files/" + self.id + "/pages")
        if r.status_code != 200:
            raise ValueError("Could not get pages from file")
        l = []
        for js in json.loads(r.text):
            l.append(Page(js))
        return l
