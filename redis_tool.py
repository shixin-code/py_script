# -*- coding: utf-8 -*-

import argparse
import sys
import log
import subprocess

parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
parser.add_argument('--room', help='specify room id. multi room id split with ","', required=True)
parser.add_argument('--platform', help='specify current live platform', choices=['agoralive', 'aestronlive'], required=True)
args = parser.parse_args()

redis_cli = '/data/services/redis.4.0.6/redis-cli'

if __name__ == '__main__':
    room_list = args.room.split(',')
    for r in room_list: 
        log.i("set room %s live platfrom to %s"%(r, args.platform))
        cmd = [redis_cli, '-h', '10.22.133.80', '-p', '19001', 'hmset', 'room-config:%s'%r, 'cur_live_platform', args.platform]
        log.i('cmd=' + ' '.join(cmd))
        subprocess.call(cmd)


