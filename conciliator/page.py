
class Page:

    id: str
    number: int
    digest: str
    type: str
    document_id: str
    split: bool

    def __init__(self, data):
        # convert types
        if data['split']: data['split'] = (  data['split'] == 'True' )
        self.__dict__ = data