from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify

import os
import netifaces

from tcpping import tcpping

app = Flask(__name__)

CONTAINER_NAME=os.uname()[1]

if 'APP_VERSION' in os.environ:
    CONTAINER_VERSION = os.environ['APP_VERSION']
else:
    CONTAINER_VERSION = "v1"

if 'APP_MESSAGE' in os.environ:
    CONTAINER_MESSAGE = os.environ['APP_MESSAGE']
else:
    CONTAINER_MESSAGE = ""

@app.route("/")
def index():
    return  render_template('index.html', container_name=CONTAINER_NAME, 
            container_version=CONTAINER_VERSION, container_message=CONTAINER_MESSAGE)


@app.route("/hello")
def hello():
    return "Hello from " + CONTAINER_NAME + " " + CONTAINER_VERSION


@app.route("/healthz")
def status():
    return jsonify(status="OK",
                   container_name=CONTAINER_NAME,
                   container_version=CONTAINER_VERSION,
                   container_message=CONTAINER_MESSAGE)


@app.route("/ping", defaults={'desthost': '127.0.0.1', 'destport':'80'})
@app.route("/ping/<desthost>", defaults={'destport': '80'})
@app.route("/ping/<desthost>/<destport>")
def tcp_ping(desthost,destport):
    # Debug enabled to get details in logs
    results=tcpping(d_host=desthost, d_port=destport, maxCount=10, DEBUG=True)
    return jsonify(container_name=CONTAINER_NAME,
                   container_version=CONTAINER_VERSION,
                   tcp_ping=results)


@app.route("/net", defaults={'ifname': 0})
@app.route("/net/<ifname>")
def pod_ifaces(ifname):
    netiflist = netifaces.interfaces()

    if ifname in netiflist:
        # invoking route /net/<ifname> with valid ifname
        try:
            ifname_addr = netifaces.ifaddresses(ifname)[netifaces.AF_INET]
        except:
            ifname_addr = ifname + " does not have a valid IPv4"

        return jsonify( container_name=CONTAINER_NAME,
                        container_version=CONTAINER_VERSION,
                        if_addr=ifname_addr)
    else:
        # invoking route /net route or not a valid ifname
        return jsonify( container_name=CONTAINER_NAME,
                        container_version=CONTAINER_VERSION,
                        if_list=netiflist)


if __name__ == "__main__":
    # to use in local 'development' environment
    # when invoked directly
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port='8080', debug=True)

#
# END OF FILE
#
