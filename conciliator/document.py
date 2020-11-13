
import json
import conciliator
import datetime
from conciliator.file import File

class Document:

    id: str
    status: str
    totalPages: int
    name: str
    entityId: str
    entityIdentifier: str
    entityName: str
    apeCode: str
    apeDescription: str
    type: str
    comment: str
    fields: object
    user_tag: object
    nb_lines: int
    lettering: str

    # ?? TODO
    emitter: str
    score: str
    pages: object
    page_image_digest: object

    # TODO: to remove
    since: datetime.datetime
    errors: object
    prepared: bool
    preparationRequired: bool
    connector_status: str
    error_status: str
    durationSoFar: int
    splittable: bool
    editionView: str
    tenantName: str
    viewName: str
    wfc: str


    @classmethod
    def list(cls, query=None):
        pass
# GET
# https://app.expert.conciliator.ai/api/v0/documents?entity_id=262929ec-a9a6-424a-a90e-f1dc3e7740fc&limit=5000&invoice_type=SALE,PURCHASE

    @classmethod
    def from_file(cls, file: File):
        # FIXME: missing call to API /documents with arg (file_id)
        # 'file_name' exists but leading to errors as name is not unique
        # fallback to file -> page -> document
        l = []
        doc_ids = []
        for page in file.pages():
            if page.document_id in doc_ids: continue
            doc_ids.append(page.document_id)
            l.append(Document.load(page.document_id))
        return l


    @classmethod
    def load(cls, doc_id:str):
        r = conciliator.session.post(conciliator.api_url + 'document/' + doc_id)
        if r.status_code != 200: raise ValueError("Cannot load document from id")
        return Document(json.loads(r.text))

    def __init__(self, data):
        # remove deprecated
        data.pop('activity', None)
        data.pop('type_activity', None)
        # convert types
        if data['fisc_start']: data['fisc_start'] = datetime.datetime.strptime(data['fisc_start'], '%Y-%m-%d').date()
        if data['fisc_end']  : data['fisc_end']   = datetime.datetime.strptime(data['fisc_end'],   '%Y-%m-%d').date()
        self.__dict__ = data


    # exclude from bank reconciliation
    def exclude(self):
        r = conciliator.session.put(conciliator.api_url + "operation/invoice/" + self.id + "exclude")
        if r.status_code != 204:
            raise ValueError("Could not exclude invoice from bank reconciliation")
        return True



#     # TODO
#     def get_data(self, payload):
#         payload = '[{"id":"goupix_invoices","pagination":{"nbItems":10,"sort":{"elements":[{"column":"since","order":"DESC"}]},"windowId":{"firstValues":null,"lastValues":null}},"filtering":{"searchTerm":null,"appliedFilters":{"entity_id":{"items":[{"value":"1bd7a243-37aa-459f-a8a6-1d406361bc30"}]}}}}]'
#         return self.session.post(self.api_url + "data", data=payload,
#                                  headers={'Content-type': "application/json"}).text
