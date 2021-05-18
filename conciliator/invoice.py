import conciliator
from conciliator.document import Document
import datetime


class Invoice(Document):

    created: str
    reference: str
    date: datetime.date
    amountInclTax: float
    amountExclTax: float
    tax: float
    supplier: str
    recipient: str
    currency: str
    exportedTimestamp: datetime.datetime
    nb_pages: int
    type_document: str
    invoice_type: str
    page_file_number: int
    lettering: str
    categories: object

    @classmethod
    def parse_response(cls, result: str):
        nb_cols = len(result['columns'])
        l = []
        for item in result['rows']:
            obj = {}
            for i in range(0, nb_cols):
                obj[result['columns'][i]['name']] = item['values'][i]['value']
            l.append(Invoice(obj))
        return l

    @classmethod
    def search(cls, query:str, nb=100, filter={}):
        data_query = Document.DATA_QUERY.copy()
        data_query[0]['pagination']['nbItems'] = nb
        data_query[0]['filtering']['searchTerm'] = query
        data_query[0]['filtering']['appliedFilters']['entity_id']['items'][0]['value'] = conciliator.current_entity.id

        for key in filter:
            # {"date": '2020-11-24'} or {"date": { "min": '2020-10-01', "max": '2020-11-01' }}
            if key == 'date':
                try:
                    d = datetime.date.isoformat(filter['date'])
                    f = { "min": d, "max": d }
                except:
                    # TODO: convert datetime.date to str
                    f = filter['date']
                data_query[0]['filtering']['appliedFilters']['date'] = f

        r = conciliator.session.post(conciliator.api_url + "data", json=data_query)
        r.raise_for_status()
        return Invoice.parse_response(r.json()[0])

    def bookentry(self):
        # GET 200 OK
        # https://app.expert.conciliator.ai/api/v0/document/1eb2e2e3-1e44-c970-ae59-38cbe272124d/entries?invoiceId=1eb2e2e3-1e44-c970-ae59-38cbe272124d


    def journal(self):
        # GET 200 OK
        # https://app.expert.conciliator.ai/api/v0/document/1eb2e2e3-1e44-c970-ae59-38cbe272124d/journal?invoiceId=1eb2e2e3-1e44-c970-ae59-38cbe272124d
        pass

    # exclude from bank reconciliation
    def exclude(self):
        r = conciliator.session.put(conciliator.api_url + "operation/invoice/" + self.id + "exclude")
        r.raise_for_status()
        return True