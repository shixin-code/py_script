# -*- coding: utf-8 -*-

import subprocess
import re
import time
import sys
import argparse
from sys import stderr
import log
import utils

parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
parser.add_argument('--room', help='specify room id. multi room id split with ","')
parser.add_argument('--room_file', help='file include room id list')
args = parser.parse_args()

if __name__ == '__main__':
    room_list = utils.parse_room_id_list(args) 
    key_count = len(room_list)
    if key_count == 0:
        parser.print_help()
        exit(0)
    index = 0
    live_platform_room = {}
    for room_id in room_list:
        index += 1
        cmd = utils.redis_cmd(['hget', 'room-config:%s'%room_id, 'cur_live_platform'])
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        stdout, stderr = p.communicate()
        plt = stdout.split('\n')[0]
        if not live_platform_room.has_key(plt):
            live_platform_room[plt] = [room_id]
        else:
            live_platform_room.get(plt).append(room_id)
        log.i(str(index) + '/' + str(key_count) + ': room ' + room_id + " platform=" + plt)
        time.sleep(0.05)
