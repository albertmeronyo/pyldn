# pyldn
A python [Linked Data Notifications (LDN)](https://linkedresearch.org/ldn/) receiver

**Author:**	Albert Meroño  
**Copyright:**	Albert Meroño, VU University Amsterdam  
**License:**	Apache 2 (see [license.txt](license.txt))

## Features
pyldn is a lightweight receiver for LDN. This means you can set up an inbox to receive notifications as Linked Data in seconds!

## Install
<pre>
git clone https://github.com/albertmeronyo/pyldn
cd pyldn
virtualenv .
source bin/activate
pip install -r requirements.txt
</pre>

## Usage
<pre>
python pyldn.py
</pre>

Then, from a client you can discover an inbox

<pre>
curl -I -X GET http://pyldn.amp.ops.labs.vu.nl/

HTTP/1.1 200 OK
Link: &lt;http://pyldn.amp.ops.labs.vu.nl:8088/inbox/&gt;;
</pre>

You can request a list of the notification URLs it contains:

<pre>
curl -X GET -H'Accept: text/turtle' http://pyldn.amp.ops.labs.vu.nl/inbox/

HTTP/1.1 200 OK

@prefix ldp: &lt;http://www.w3.org/ns/ldp#&gt; .
@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .
@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .

&lt;http://pyldn.amp.ops.labs.vu.nl:8088/inbox/&gt; a ldp:BasicContainer,
        ldp:Container,
        ldp:RDFSource,
        ldp:Resource ;
    ldp:contains &lt;http://pyldn.amp.ops.labs.vu.nl:8088/inbox/1&gt;,
        &lt;http://pyldn.amp.ops.labs.vu.nl:8088/inbox/2&gt; .
</pre>

You can even post new notifications to this inbox! You'll get the URL for your notification in the response headers:

<pre>
curl -i -X POST -d '<foo> <bar> <foobar> .' -H'Content-Type: text/turtle' http://pyldn.amp.ops.labs.vu.nl/inbox/

HTTP/1.1 201 CREATED
Location: http://pyldn.amp.ops.labs.vu.nl:8088/inbox/3
</pre>

If you want to retrieve the content of your brand new notification:

<pre>
curl -i -X GET -H'Accept: text/turtle' http://pyldn.amp.ops.labs.vu.nl/inbox/3

HTTP/1.1 200 OK

@prefix ns1: &lt;file:///home/amp/src/pyldn/&gt; .
@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .
@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .

ns1:foo ns1:bar ns1:foobar .
</pre>

See the [latest LDN draft](https://linkedresearch.org/ldn/) for a complete and concise description of all you can do with LDN!

## Configuration
You'll find a sample [config.ini](config.ini) file you can customize according to your needs (mostly base path, inbox path, and port).
