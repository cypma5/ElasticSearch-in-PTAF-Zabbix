#!/usr/bin/python
# coding=utf-8

from elasticsearch import Elasticsearch
import json
import os
import sys
import time
import socket 


"""
Zabbix agent script for consuming ElasticSearch metrics
"""

__author__ = "Adel Sachkov <adel.sachkov@yandex.ru>"
__date__ = "13 May 2018"
__version__ = "$Revision: 2.2 $"
__fork__ = "Telegram: @KH93b"


#нужна переменная
#es_host = '$(hostname)'
es_host =  socket.gethostname()
es_port = 9200
cache = '/opt/es_zabbix/es_zabbix-{0}.json'
cache_ttl = 55

f = open('/opt/waf/conf/master_password', 'r')
for line in f:
    line = line.rstrip('\n')
    http_auth=("root",line)
f.close()
line = line.rstrip('\n')


def es_connect(host, port, timeout=30):
    try:
        con = Elasticsearch(host=es_host, port=port, http_auth=http_auth , timeout=timeout)
#http_auth нужно брать из файла  /opt/waf/conf/master_password 


    except Exception as e:
        print "Elasticsearch connection error.", e
        return False
    return con


def get_es_api_cache(con, api, cache_file, ttl=55):
    api_set = {
        'cluster': con.cluster.stats,
        'health': con.cluster.health,
        'indices': con.indices.stats,
        'nodes': con.nodes.stats
    }
    if os.path.exists(cache_file) and time.time() - os.path.getmtime(cache_file) < ttl:
        return json.load(open(cache_file, 'r'))
    else:
        if api not in api_set.keys():
            return False
        else:
            data = api_set[api]()
            json.dump(data, open(cache_file, 'w'))
            return data


def get_es_metrics(con, api, key):
    cache_file = cache.format(api)
    api_data = get_es_api_cache(con, api, cache_file, cache_ttl)
    for k in key.split(':'):
        if k in api_data.keys():
            api_data = api_data[k]
        else:
            return 'Unsupported key'
    return api_data


def discover_nodes(con, node_id=None):
    zabbix_json = {'data': []}
    api_data = get_es_metrics(con, 'nodes', 'nodes')
    if node_id:
        zabbix_json['data'].append({'{#NAME}': api_data[node_id]['name'], '{#NODE}': node_id})
    else:
        for k in api_data.keys():
            zabbix_json['data'].append({'{#NAME}': api_data[k]['name'], '{#NODE}': k})
    return json.dumps(zabbix_json)


def discover_indices(con):
    zabbix_json = {'data': []}
    api_data = get_es_metrics(con, 'indices', 'indices')
    for k in api_data.keys():
        zabbix_json['data'].append({'{#NAME}': k})
    return json.dumps(zabbix_json)


if __name__ == '__main__':
    es_api = None
    es_key = None

    if len(sys.argv) < 3:
        print 'Usage: es_zabbix.py [api|discover] key:subkey:subkey'
        exit(1)
    else:
        es_api = sys.argv[1]
        es_key = sys.argv[2]

    es = es_connect(es_host, es_port)

    if es_api == 'discover' and es_key == 'nodes':
        print discover_nodes(es)
    elif es_api == 'discover' and es_key == 'node':
        node = ''.join(es.nodes.stats('_local')['nodes'].keys())
        print discover_nodes(es, node)
    elif es_api == 'discover' and es_key == 'indices':
        print discover_indices(es)
    else:
        print get_es_metrics(es, es_api, es_key)
