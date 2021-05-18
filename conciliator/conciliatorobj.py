import json
import datetime
import typing
import inspect

class ConciliatorObj:

    def __init__(self, data):
        self.__dict__ = self.deserialize(data)

    def deserialize(self, data):

        types = {}
        for klass in inspect.getmro(self.__class__):
            if klass == ConciliatorObj: break
            types.update(typing.get_type_hints(klass))

        for k in list(data.keys()):
            if k in types:
                t = types[k]
                # date
                if t == datetime.date:
                    try:
                        data[k] = datetime.datetime.strptime(data[k] , '%Y-%m-%d').date()
                    except:
                        pass
                # datetime
                elif t == datetime.datetime:
                    try:
                        # adding trailing zeros that are removed by Conciliator API
                        data[k] = datetime.datetime.fromisoformat(
                            data[k].replace('Z', '+00:00') + '0' * (26 - len(data[k])))
                    except:
                        data.pop(k, None)
                # bool
                elif t == bool:
                    if isinstance(data[k], bool):
                        continue
                    try:
                        data[k] = (data[k].lower() == 'true')
                    except:
                        data.pop(k, None)
            else:
                data.pop(k, None)
        return data

    def serialize(self):

        types = typing.get_type_hints(self)
        data = {}

        for k in types:
            t = types[k]
            v = getattr(self, k, None)
            if t == datetime.date and v:
                try:
                    data[k] = datetime.date.isoformat(v)
                except:
                    pass
            elif t == datetime.datetime and v:
                try:
                    data[k] = datetime.datetime.isoformat(v)
                except:
                    pass
            elif v:
                data[k] = v
        return data

    def serializes(self):
        return json.dumps(self.serialize())
