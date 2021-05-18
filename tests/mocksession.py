import requests
import pickle
import conciliator
from slugify import slugify
import os
import re

class MockSession(requests.Session):

    storepath: str

    def pkl_name(self, url:str):
        # remove baseurl and IDs, clean and shorten
        url = url.replace(conciliator.api_url, '')
        url = re.sub('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 'id', url)
        return  os.path.join(self.storepath, slugify(url)[0:60] + '.pkl')


class RecordSession(MockSession):


    def record(self, r:requests.Response, url:str):
        try:
            os.mkdir(self.storepath)
        except FileExistsError:
            pass
        filename = self.pkl_name(url)
        if os.path.exists(filename):
            print("Warning: file already exists")
        print(filename, url)
        f = open(filename, 'wb')
        # FIXME: remove password before saving
        # value key in r.request.body
        # b'{"type": "basic", "value": "cGRlY2hhc3RlbGxpZXJAZ21haWwuY29tOmx1Y3VsdVM2OA==", "accountStore": {"href": "https://sso.dhatim.com/id/api/v1/applications/8b96be0c-d3c3-4149-a5a5-556a388a0780"}}'
        pickle.dump(r, f)
        f.close()

    def get(self, url, **kwargs):
        r = super().get(url, **kwargs)
        self.record(r, url)
        return r

    def post(self, url, **kwargs):
        r = super().post(url, **kwargs)
        self.record(r, url)
        return r

    def put(self, url, **kwargs):
        r = super().put(url, **kwargs)
        self.record(r, url)
        return r

    def patch(self, url, **kwargs):
        r = super().patch(url, **kwargs)
        self.record(r, url)
        return r


class ReplaySession(MockSession):

    def load_response(self, url):
        filename = self.pkl_name(url)
        f = open( filename, 'rb')
        pkl = pickle.load(f)
        f.close()
        return pkl

    def get(self, url, **kwargs):
        return self.load_response(url)

    def post(self, url, **kwargs):
        return self.load_response(url)

    def put(self, url, **kwargs):
        return self.load_response(url)

    def patch(self, url, **kwargs):
        return self.load_response(url)