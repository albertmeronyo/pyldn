#!/usr/bin/env python

# config.py: An object to manage pyldn's config

from ConfigParser import SafeConfigParser
import logging

clog = logging.getLogger(__name__)

class Pyldnconfig(object):
    def __init__(self):
        '''
        Class constructor
        '''
        CONFIG_INI = 'config.ini'
        config = SafeConfigParser()
        config.read(CONFIG_INI)

        self._base_path = config.get('ldn', 'basePath')
        self._inbox_path = config.get('ldn', 'inboxPath')
        self._port = int(config.get('ldn', 'port'))

        if not self._base_path:
            self._base_path = 'http://localhost'
        if not self._inbox_path:
            self._inbox_path = '/inbox/'
        if not self._port:
            self._port = 80

        port_str = ":" + str(self._port) if self._port != 80 else ""
        self._inbox_url = self._base_path + port_str + self._inbox_path

        self._ldn_counter = 1

    def log_config(self):
        clog.info('Current pyldn configuration')
        clog.info('Base path: {}'.format(self._base_path))
        clog.info('Inbox path: {}'.format(self._inbox_path))
