import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
import time, threading

from flask import Flask, Response

import time


# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
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


app = Flask(__name__, static_url_path='', static_folder='../web')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
subscriptions = []


def notify():
    msg = " => Server says hi!" + str(time.time())
    for sub in subscriptions[:]:
        sub.put(msg)


@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)


@app.route("/publish")
def publish():
    gevent.spawn(notify)

    return "OK"


@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
