import json

class BaseMsg(object):

    def __init__(self, form=None, payload=None):
        self.form = form
        self.payload = payload

    def to_dict(self) -> dict:
        raise NotImplementedError


class BaseProtocol(object):

    def pack(self, form, payload) -> str:
        raise NotImplementedError

    def unpack(self, string: str):
        raise NotImplementedError

    def process_request(self, req) -> (str, bool):
        msg = self.unpack(req)

        try:
            res, end = getattr(self, "do_%s" % msg.form)(msg.payload)
        except AttributeError:
            res, end  = ('error', "Could not process '%s'" % msg.form), False

        return self.pack(*res), end


class JsonMsg(BaseMsg):

    def to_dict(self) -> dict:
        return {
            'form': self.form,
            'payload':self. payload
        }


class JsonProtocol(BaseProtocol):

    def pack(self, form, payload) -> str:
        return json.dumps(JsonMsg(form, payload).to_dict())

    def unpack(self, string: str):
        try:
            data = json.loads(string)
            form, protocol = data['form'], data.get('payload', None)
        except ValueError:
            form, protocol = 'error', string

        return JsonMsg(form, protocol)
