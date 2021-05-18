
import json
import conciliator
import datetime

class Document:

    id: str
    status: str
    totalPages: int
    name: str
    type: str
    comment: str
    fields: object
    user_tag: object
    nb_lines: int

    DATA_QUERY = [{
        "id": "goupix_invoices",
        "pagination": {
            "sort": {
                "elements": [
                    {
                        "column": "created",
                        "order": "DESC"
                    },
                    {
                        "column": "page_file_number",
                        "order": "ASC"
                    }
                ]
            },
            "windowId": {
                "firstValues": None,
                "lastValues": None
            }
        },
        "filtering": {
            "appliedFilters": {
                "entity_id": {
                    "items": [
                        {
                            "value": "<entity_id>"
                        }
                    ]
                }
            }
        }
    }]


    @classmethod
    def list(cls, query=None):
        pass
# GET
# https://app.expert.conciliator.ai/api/v0/documents?entity_id=262929ec-a9a6-424a-a90e-f1dc3e7740fc&limit=5000&invoice_type=SALE,PURCHASE

    # @classmethod
    # def from_filepages(cls, file: File):
    #     # FIXME: missing call to API /documents with arg (file_id)
    #     # 'file_name' exists but leading to errors as name is not unique
    #     # fallback to file -> page -> document
    #     l = []
    #     doc_ids = []
    #     for page in file.pages():
    #         if page.document_id in doc_ids: continue
    #         doc_ids.append(page.document_id)
    #         l.append(Document.load(page.document_id))
    #     return l

    @classmethod
    def load(cls, doc_id:str):
        r = conciliator.session.post(conciliator.api_url + 'document/' + doc_id)
        if r.status_code != 200: raise ValueError("Cannot load document from id")
        return Document(json.loads(r.text))

    def __init__(self, data):
        # TODO convert types
        self.__dict__ = data

    @property
    def pdf(self):
        r = conciliator.session.get(conciliator.api_url + 'document/' + self.id + '/download')
        if r.status_code != 200: raise ValueError("Cannot download PDF for document")
        return r.content






#     # TODO
#     def get_data(self, payload):
#         payload = '[{"id":"goupix_invoices","pagination":{"nbItems":10,"sort":{"elements":[{"column":"since","order":"DESC"}]},"windowId":{"firstValues":null,"lastValues":null}},"filtering":{"searchTerm":null,"appliedFilters":{"entity_id":{"items":[{"value":"1bd7a243-37aa-459f-a8a6-1d406361bc30"}]}}}}]'
#         return self.session.post(self.api_url + "data", data=payload,
#                                  headers={'Content-type': "application/json"}).text
