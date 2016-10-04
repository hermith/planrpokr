import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from flask import Flask, Response
import time

from connectivity.server import ServerSentEvent
from user.user import User

app = Flask(__name__, static_url_path='', static_folder='../web')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
subscriptions = []


def notify():
    msg = " => Server says hi!" + str(time.time())
    for sub in subscriptions[:]:
        sub.queue.put(msg)


@app.route("/debug")
def debug():
    subs = "Currently %d subscriptions:<br/>" % len(subscriptions)
    for sub in subscriptions:
        subs += str(sub.uuid) + "<br/>"

    return subs


@app.route("/publish")
def publish():
    gevent.spawn(notify)

    return "OK"


@app.route("/subscribe")
def subscribe():
    def gen():
        q = User(Queue())
        subscriptions.append(q)
        q.queue.put({'uuid': str(q.uuid)})
        try:
            while True:
                result = q.queue.get()
                ev = ServerSentEvent(result)
                yield ev.encode()
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
