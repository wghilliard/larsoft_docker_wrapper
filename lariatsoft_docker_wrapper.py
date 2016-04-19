__author__ = "William Hilliard"
# Version: Chance
# Syntax: python larsoft_docker_wrapper.py {{mount_point}} {{preset}} {{cpu_count}} {{event_count}}
# NOTE: Please make sure you have rw permissions for the mount_point. It is prefferable for it to be empty.

import sys
import os
import subprocess as sp
from subprocess import Popen, PIPE
#from docker import Client
import datetime
import argparse
import shutil

#IMAGE = 'wghilliard/lariatsoft_wrapped:latest'
IMAGE = 'wghilliard/test:latest'
DEBUG = False

parser = argparse.ArgumentParser(description="A utlity to spin up and direct output of lariatsoft docker containers.")
parser.add_argument('mount_point', help='the output directory where a subdirectory named after the current linux epoch will be created')
parser.add_argument('preset', help='the file which contains commands to be run inside the docker images, reference /products/presets/')
parser.add_argument('container_count', help='the number of containers to create, lariatsoft is single threaded so 1 container per cpu is advised')
parser.add_argument('event_count', type=int, help='the number of events per container to generate')
parser.add_argument('-n', '--new_file', default=None, help='the fickle file to run instead of the preset default')

#cli = Client(base_url='unix://var/run/docker.sock')
preset_list =['one']

def get_time():
    lol = datetime.datetime.now()
    return lol.strftime('%s')

def dispatch(mount_point, cmd):
    if DEBUG: print(cmd)
    # NOTE Need to clean up after with --rm flag.
    p = sp.call('docker run -dv {0}:/data {2} /bin/bash -c {1}'.format(mount_point, cmd, IMAGE), shell=True)
    return

def core(mount_point, preset, cpu_count, event_count, new_file):

    try:
        print("Running preliminary checks...")
       # if int(cpu_count) > int(cli.info()['NCPU']):
       #    print("CPU_COUNT is set to {0} and the max is {1}.".format(cpu_count, cli.info()['NCPU']))
       #    return False

#        event_per_cont = int(event_count / cpu_count)

        if not os.path.isdir(mount_point):
           print("There are issues with the mount_point '{0}', please check it and try again!".format(mount_point))
           return False

        if preset not in preset_list:
           print("Preset not recognized! I only accept {0}.".format(preset_list))
           return False
        print("Marking territory...")
        time = get_time()
        mount_point = os.path.join(mount_point, time)
        print('Output will be saved to {0}...'.format(mount_point))
        os.mkdir(mount_point)
        
        if new_file != None:
            try:
                if  os.path.isfile(new_file):
                    shutil.copy(new_file, mount_point)
                    new_file = new_file.split('/')[-1]
                    print('Using {0} instead of default fickle file...').format(new_file)
                else:
                    print("{0} cannot be copied, aborting...".format(new_file))
                    return
            except Exception as e:
                print(e)
                return
   
        container_list = list()
        print("Spinning up containers")
        for count in range(int(cpu_count)):
           cmd = '\'source /etc/lariatsoft_setup.sh && python /products/presets/{0}.py {1} {2} {3}\''.format(preset, count, event_count, new_file if new_file != None else ' ')
           dispatch(mount_point, cmd)
        print("The containers are loose!")
        print("Use 'docker stats' to track their progress!")
        return True

    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    args = parser.parse_args()
    #core(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    core(args.mount_point, args.preset, args.container_count, args.event_count, args.new_file)
