# -*- coding: utf-8 -*-

import argparse
import sys
import log
import subprocess

parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
parser.add_argument('--room', help='specify room id. multi room id split with ","')
parser.add_argument('--room_file', help='file include room id list')
parser.add_argument('--enable', action="store_true", dest='enable', help='enable local record')
parser.add_argument('--disable', action="store_false", dest='enable', help='disenable local record')
args = parser.parse_args()
parser.set_defaults(enable=True)

redis_cli = '/data/services/redis.4.0.6/redis-cli'

if __name__ == '__main__':
    room_list = []
    if args.room != None:
     room_list = args.room.split(',')

    if args.room_file != None:
        with open(args.room_file, 'r') as f:
            room_list.extend(f.readlines())   

    log.i('room id list=' + '|'.join(room_list))
    i = 0
    for r in room_list: 
        i += 1
        log.i("set room %s local record to %s"%(r, args.enable))
        val = 1 if args.enable else 0
        config = '{"enable_local_record":%s,"disk_free_notify":2}'%(val)
        cmd = [redis_cli, '-h', '10.22.133.80', '-p', '19001', 'hmset', 'room-config:%s'%r, 'local_record_config', config]
        log.i(str(i) + '. cmd=' + ' '.join(cmd))
        subprocess.call(cmd)


