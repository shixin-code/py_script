# -*- coding: utf-8 -*-

import subprocess
import re
import time
from sys import stderr
import log
import redis_config

if __name__ == '__main__':
    cmd = [redis_config.redis_cli, '-h', redis_config.redis_server, '-p', redis_config.redis_port, 'keys', 'room-config:*']
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
    
    stdout, stderr = p.communicate()
    log.i('stderr=' + stderr)
    keys = stdout.split('\n')

    key_count = len(keys)
    index = 0
    live_platform_room = {}
    for key in keys:
        index += 1
        room_id = re.findall(r'\d+', key)
        if len(room_id) == 0:
            log.i('invalid room id:' + key)
            continue
        cmd = [redis_config.redis_cli, '-h', redis_config.redis_server, '-p', redis_config.redis_port, 'hget', key, 'cur_live_platform']
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        stdout, stderr = p.communicate()
        plt = stdout.split('\n')[0]
        if not live_platform_room.has_key(plt):
            live_platform_room[plt] = room_id
        else:
            live_platform_room.get(plt).extend(room_id)
        log.i(str(index) + '/' + str(key_count) + ': get key=' + key + ", platform=" + plt)
        time.sleep(0.05)

    for key in live_platform_room.keys():
        log(key + "=" + ','.live_platform_room[key])
    