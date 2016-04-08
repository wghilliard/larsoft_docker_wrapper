import os
import sys
import subprocess as sp
import datetime

def core(cont_count, event_count):
    os.chdir('/data')
    exec_list = ['lar -c /products/dev/prodsingle_lariat.fcl -n {0} -o single_gen_{1}.root'.format(event_count, cont_count),
                 'lar -c /products/dev/WireDump_numu_NC-1.fcl -s single_gen_{0}.root -T wire_dump_out_{0}.root'.format(cont_count)]
    for cmd in exec_list:
        print(cmd)
        sp.call(cmd, shell=True)
    return

if __name__ == '__main__':
    core(sys.argv[1], sys.argv[2])
