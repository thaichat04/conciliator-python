from conciliator.conciliatorobj import ConciliatorObj

class Page(ConciliatorObj):

    id: str
    number: int
    digest: str
    type: str
    document_id: str
    split: bool
