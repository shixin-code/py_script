# -*- coding: utf-8 -*-

import argparse
import sys
import log
import subprocess
import os.path
import json
import io

parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
parser.add_argument('--versionfile', help='version file', required=True)
parser.add_argument('--notest', help='use test enviroment', action='store_true')
args = parser.parse_args()

redis_cli = '/data/services/redis.4.0.6/redis-cli'

def get_desc(desc_file):
    log.i('load desc file:' + desc_file)
    with io.open(desc_file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        return ''.join(lines)
    return ''

def to_version_id(version):
    kVersionFieldCount = 4;
    items = version.split('.')
    while len(items) < kVersionFieldCount:
        items.append('0')
    
    version_id = pow(10, 8)
    for i in range(kVersionFieldCount):
        factor = (kVersionFieldCount - i - 1) * 2
        version_id += int(items[i]) * pow(10, factor)
    log.i('version %s --> versionId %d' % (version, version_id))
    return version_id
    

if __name__ == '__main__': 
    host = '10.22.133.80' if args.notest else '10.22.130.89'
    file_path = os.path.abspath(args.versionfile)
    file_dir, file_name = os.path.split(file_path)
    log.i('version config file=' + file_path)
    log.i('version file dir=' + file_dir + ", " + file_name)
    with open(file_path,'r') as f:
        version_data = json.load(f)
        def_data = version_data.get('default')
        def_version = def_data.get('version')
        def_desc_file = def_data.get('desc_file')
        def_pub_date = def_data.get('pub_date')
        def_update_type =def_data.get('update_type', 0)
        platforms = version_data.get('platform')
        for plt_version_data in platforms:
            platform = plt_version_data['platform']
            log.i('upgrad ' + platform + "----------------")
            version = plt_version_data.get('version', def_version)
            desc_file = plt_version_data.get('desc_file', def_desc_file)
            download_url = plt_version_data.get('url') 
            pub_date = plt_version_data.get('pub_date', def_pub_date)
            md5 = plt_version_data.get('md5')
            size = plt_version_data.get('size')
            update_type = plt_version_data.get('update_type', def_update_type)
            log.i('download url=' + download_url)
            log.i('md5=' + md5)
            log.i('size=' + str(size))
            log.i('pub date=' + pub_date)
            log.i('desc file=' + desc_file)
            cmd = [redis_cli, '-h', host, '-p', '19001', 'hmset', 'cur_cli_ver:teacherapp:%s'%platform, "version", version,
                'versionId', str(to_version_id(version)), "downUrl", download_url, 'desc', get_desc(os.path.join(file_dir, desc_file)), 
                'pubDate', pub_date, 'md5', md5, 'size', str(size), 'updateType', str(update_type)]
            print(cmd)
            subprocess.check_call(cmd)
            # log.i('cmd=' + ' '.join(cmd))

    
