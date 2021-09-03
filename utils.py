# -*- coding: utf-8 -*-

import argparse
import redis_config

def parse_room_id_list(args):
    room_list = []
    if args.room != None:
     room_list = args.room.split(',')

    if args.room_file != None:
        with open(args.room_file, 'r') as f:
            content = f.read()
            room_list.extend(content.split('\r\n'))   
    return room_list

def redis_cmd(cmd):
    full_cmd = [redis_config.redis_cli, '-h', redis_config.redis_server, '-p', redis_config.redis_port]
    full_cmd.extend(cmd)
    return full_cmd
