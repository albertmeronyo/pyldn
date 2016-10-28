# pyldn
A python [Linked Data Notifications (LDN)](https://github.com/w3c/ldn) receiver

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

## Configuration
You'll find a sample [config.ini](config.ini) file you can customize according to your needs (mostly base path, inbox path, and port).
