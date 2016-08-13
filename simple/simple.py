#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Aug 13, 2016 '
__author__= 'samuel'

import boto
import boto.s3.connection

from flask import Flask
from flask import render_template
app = Flask(__name__)

access_key = ''
secret_key = ''
ceph_host = ''
ceph_port = 7480


@app.route('/')
def index():
    items = [{
        'bucket_name': 'demo-bucket',
        'keys':[
            {'key_name': 'demo-key'}
            ]
        }]
    conn = ceph_connect()
    buckets = ceph_list_buckets(conn)
    items = []
    for b in buckets:
        bucket = {}
        bucket['bucket_name'] = b
        bucket['keys'] = [{'key_name': k} for k in ceph_list_keys(conn, b)]
        items.append(bucket)
    return render_template('index.jinja2', items=items)


@app.route('/<bucket_name>')
def bucket(bucket_name):
    conn = ceph_connect()
    buckets = ceph_list_buckets(conn)
    if not bucket_name in buckets:
        return 'Bucket(%s) is not exist.' % bucket_name
    buckets = [bucket_name]
    items = []
    for b in buckets:
        bucket = {}
        bucket['bucket_name'] = b
        bucket['keys'] = [{'key_name': k} for k in ceph_list_keys(conn, b)]
        items.append(bucket)
    return render_template('index.jinja2', items=items)


def ceph_connect():
    conn = boto.connect_s3(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            host=ceph_host,
            port=ceph_port,
            is_secure=False,
            calling_format=boto.s3.connection.OrdinaryCallingFormat()
            )
    return conn


def ceph_list_buckets(conn):
    buckets = conn.get_all_buckets()
    return [ x.name for x in buckets ]


def ceph_list_keys(conn, bucket_name):
    bucket = conn.get_bucket(bucket_name)
    keys = bucket.get_all_keys()
    return [x.name for x in keys]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

