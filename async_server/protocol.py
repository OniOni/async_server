import json

class BaseProtocol(object):

    def __init__(self, form=None, payload=None):
        self.form = form
        self.payload = payload

    def to_dict(self):
        raise NotImplementedError

class JsonProtocol(BaseProtocol):

    def to_dict(self):
        return {
            'form': self.form,
            'payload':self. payload
        }

def pack(obj: BaseProtocol) -> str:
    return json.dumps(obj.to_dict())

def unpack(string: str) -> BaseProtocol:
    try:
        data = json.loads(string)
        form, protocol = data['form'], data.get('payload', None)
    except ValueError:
        form, protocol = 'error', None

    return JsonProtocol(form, protocol)
