import os
from collections import defaultdict
import copy

from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_bootstrap import Bootstrap
from config import set_mqtt_config

app = Flask(__name__)
set_mqtt_config(app)
mqtt = Mqtt(app)
bootstrap = Bootstrap(app)

class MqttDashboardServer(object):
    def __init__(self):
        self._keys = []
        self._current_key = ""
        self._messages = []
        self.messages = defaultdict(list)

    def add_payload(self,message):
        self.messages[message["topic"]].append(message["payload"])

    def __len__(self):
        total_count = sum([len(v) \
                           for k,v in \
                           self.messages.items()])
        return total_count

    def __repr__(self):
        return f"Dashboard server with total count of messages : {len(self)}"

    def message_generator(self):
        for topic, payloads in self.messages.items():
            for payload in payloads:
                yield topic, payload

mqtt_server = MqttDashboardServer()

@mqtt.on_connect()
def handle_connect(client, userdata, flags,rc):
    mqtt.subscribe("test")

@mqtt.on_message()
def handle_mqtt_message(client,userdata,message):
    #print(f"message dir {dir(message)})")
    #print(f"client dir {dir(client)})")
    #print(f"userdata dir {dir(userdata)})")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    mqtt_server.add_payload(data)

@app.route("/")
def hello():
    return f"Hello from Python! I've got a mqtt server {mqtt_server}"

@app.route("/dashboard")
def dashboard():
    print(f"rendering dashboard {mqtt_server}")
    message_tuples = [(k,v) for k,v in mqtt_server.message_generator()]
    return render_template('dashboard.html', message_tuples = message_tuples)

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host='localhost',port=port)
