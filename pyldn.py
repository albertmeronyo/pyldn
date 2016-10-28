#!/usr/bin/env python

# pyldn: A python Linked Data Notifications (LDN) receiver

from flask import Flask, request, render_template, make_response
import logging
import requests
from rdflib import Graph, URIRef, RDF, Namespace

# pyldn modules
from pyldnconfig import Pyldnconfig

# The Flask app
app = Flask(__name__)

# Logging
LOG_FORMAT = '%(asctime)-15s [%(levelname)s] (%(module)s.%(funcName)s) %(message)s'
app.debug_log_format = LOG_FORMAT
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
pyldnlog = logging.getLogger(__name__)

# Config
pyldnconf = Pyldnconfig()
pyldnlog.info(pyldnconf.log_config())

# Accepted content types
ACCEPTED_TYPES = ['application/ld+json',
                  'text/turtle',
                  'application/ld+json; profile="http://www.w3.org/ns/activitystreams']

# Graph of the local inbox
ldp_url = URIRef("http://www.w3.org/ns/ldp#")
ldp = Namespace(ldp_url)

inbox_graph = Graph()
inbox_graph.add((URIRef(pyldnconf._inbox_url), RDF.type, ldp['Resource']))
inbox_graph.add((URIRef(pyldnconf._inbox_url), RDF.type, ldp['RDFSource']))
inbox_graph.add((URIRef(pyldnconf._inbox_url), RDF.type, ldp['Container']))
inbox_graph.add((URIRef(pyldnconf._inbox_url), RDF.type, ldp['BasicContainer']))
inbox_graph.bind('ldp', ldp)

# Dict for the notification graphs
# keys = graph names, values = rdflib.Graph()
graphs = {}

# Server routes
@app.route('/', methods=['GET', 'POST'])
def pyldn():
    resp = make_response(render_template('index.html'))
    resp.headers['X-Powered-By'] = 'https://github.com/albertmeronyo/pyldn'
    resp.headers['Link'] =  '<' + pyldnconf._inbox_url + '>; rel="http://www.w3.org/ns/ldp#inbox", <http://www.w3.org/ns/ldp#Resource>; rel="type", <http://www.w3.org/ns/ldp#RDFSource>; rel="type"'

    return resp

@app.route(pyldnconf._inbox_path, methods=['HEAD'])
def head_inbox():
    resp = make_response()
    resp.headers['X-Powered-By'] = 'https://github.com/albertmeronyo/pyldn'
    resp.headers['Allow'] = "GET, HEAD, OPTIONS, POST"
    resp.headers['Link'] = '<http://www.w3.org/ns/ldp#Resource>; rel="type", <http://www.w3.org/ns/ldp#RDFSource>; rel="type", <http://www.w3.org/ns/ldp#Container>; rel="type", <http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'
    resp.headers['Accept-Post'] = 'application/ld+json, text/turtle'

    return resp

@app.route(pyldnconf._inbox_path, methods=['GET'])
def get_inbox():
    pyldnlog.debug("Requested inbox data of {} in {}".format(request.url, request.headers['Accept']))
    if not request.headers['Accept'] or request.headers['Accept'] == '*/*':
        resp = make_response(inbox_graph.serialize(format='application/ld+json'))
    elif request.headers['Accept'] in ACCEPTED_TYPES:
        resp = make_response(inbox_graph.serialize(format=request.headers['Accept']))
    else:
        return 'Requested format unavailable', 415

    resp.headers['X-Powered-By'] = 'https://github.com/albertmeronyo/pyldn'
    resp.headers['Allow'] = "GET, HEAD, OPTIONS, POST"
    resp.headers['Link'] = '<http://www.w3.org/ns/ldp#Resource>; rel="type", <http://www.w3.org/ns/ldp#RDFSource>; rel="type", <http://www.w3.org/ns/ldp#Container>; rel="type", <http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'
    resp.headers['Accept-Post'] = 'application/ld+json, text/turtle'

    return resp

@app.route(pyldnconf._inbox_path, methods=['POST'])
def post_inbox():
    # Check if there's acceptable content
    if request.headers['Content-Type'] not in ACCEPTED_TYPES:
        return 'Content type not accepted', 500
    if not request.data:
        return 'Received empty payload', 500

    resp = make_response()

    ldn_url = pyldnconf._inbox_url + str(pyldnconf._ldn_counter)
    graphs[ldn_url] = g = Graph()
    try:
        g.parse(data=request.data, format=request.headers['Content-Type'])
    except: # Should not catch everything
        return 'Could not parse received {} payload'.format(request.headers['Content-Type']), 500

    pyldnlog.debug('Created notification {}'.format(ldn_url))
    inbox_graph.add((URIRef(pyldnconf._inbox_url), ldp['contains'], URIRef(ldn_url)))
    resp.headers['Location'] = ldn_url
    pyldnconf._ldn_counter += 1

    return resp, 201

@app.route(pyldnconf._inbox_path + '<id>', methods=['GET'])
def get_notification(id):
    pyldnlog.debug("Requested notification data of {} in {}".format(request.url, request.headers['Accept']))

    # Check if the named graph exists
    pyldnlog.debug("Dict key is {}".format(pyldnconf._inbox_url + id))
    if pyldnconf._inbox_url + id not in graphs:
        return 'Requested notification does not exist', 404

    if not request.headers['Accept'] or request.headers['Accept'] == '*/*':
        resp = make_response(graphs[pyldnconf._inbox_url + id].serialize(format='application/ld+json'))
    elif request.headers['Accept'] in ACCEPTED_TYPES:
        resp = make_response(graphs[pyldnconf._inbox_url + id].serialize(format=request.headers['Accept']))
    else:
        return 'Requested format unavailable', 415

    resp.headers['X-Powered-By'] = 'https://github.com/albertmeronyo/pyldn'
    resp.headers['Allow'] = "GET"

    return resp

if __name__ == '__main__':
    app.run(8088, debug=True)
