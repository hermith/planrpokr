import json


class ServerSentEvent(object):
    def __init__(self, data):
        self.data = SSEData(data)
        self.event = None
        self.id = None
        self.desc_map = {
            self.data: "data",
            self.event: "event",
            self.id: "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.items() if k]

        return "%s\n\n" % "\n".join(lines)


class SSEData:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return json.dumps(self.data)
