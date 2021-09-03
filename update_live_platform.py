# -*- coding: utf-8 -*-

import argparse
import sys
import subprocess
import log
import utils

parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
parser.add_argument('--room', help='specify room id. multi room id split with ","')
parser.add_argument('--room_file', help='file include room id list')
parser.add_argument('--platform', help='specify current live platform', choices=['agoralive', 'aestronlive'], required=True)
args = parser.parse_args()

redis_cli = '/data/services/redis.4.0.6/redis-cli'

if __name__ == '__main__':
    room_list = utils.parse_room_id_list(args) 
    log.i('room id list=' + '|'.join(room_list))
    i = 0
    for r in room_list: 
        i += 1
        log.i(str(i) + " set room [%s] live platfrom to [%s] ---------------"%(r, args.platform))
        cmd = utils.redis_cmd(['hmset', 'room-config:%s'%r, 'cur_live_platform', args.platform])
        log.i('cmd=' + ' '.join(cmd))
        subprocess.call(cmd)


