#!/usr/bin/python3

import sys
from tuyapy import TuyaApi
import os
import time
import json
import subprocess

api = TuyaApi()

def reload_smartsocket(plug_config):

    with open(plug_config) as config:
        data = json.load(config)

    username,password,country_code,application,sw_device,ping_perf = data['username'],data['password'],data['country_code'],data['application'],data['sw_device'],data['ping_perf']
    api.init(username,password,country_code,application)
    device_ids = api.get_all_devices()
    my_sw_obj = dict((i.name(),i) for i in device_ids if i.obj_type == 'switch' and i.name() == sw_device)
    result = subprocess.run(ping_perf, shell=True, stdout=subprocess.PIPE, encoding='UTF-8')
    dev_state = my_sw_obj[sw_device].state()
    print(dev_state, result.stdout)

    if result.returncode !=0 and dev_state == True:
        my_sw_obj[sw_device].turn_off()
        print('Beeline is down!')
        time.sleep(5)
        my_sw_obj[sw_device].turn_on()
        time.sleep(7)
        dev_state = my_sw_obj[sw_device].state()
        print(dev_state, 'Router restarted!')
    elif dev_state == False:
        my_sw_obj[sw_device].turn_on()
        print('Switch was disabled! Enabled!')
    else:
        print('All is ok!')


if __name__ == "__main__":
    reload_smartsocket('/home/phil/tuya/config.json')
