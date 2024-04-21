import jsonpickle
from tunefinder.definitions.Destination import Destination
from tunefinder.definitions.Source import Source


def encode_json(obj):
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    return jsonpickle.encode(obj, unpicklable=False, indent=4)


class Result:
    def __init__(self, source: Source, destination: Destination, result):
        self.source = source
        self.destination = destination
        self.result = result

    def toJSON(self, minimal: bool = False):
        if (minimal):
            return encode_json(dict(result=self.result))
        return encode_json(self)

    def toTXT(self):
        return "\n".join(result.url for result in self.result)
