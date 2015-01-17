#!/usr/bin/python
"""Spin up a webserver

Usage:
  webserve.py start WEBSERVER_NAME [options]
  webserve.py stop WEBSERVER_NAME
  webserve.py (-h | --help)

Options;
  -d --dir=DIRECTORY_TO_SERVE  Path of directory to be served [default: ./]
  -p --port=PORT               HTTP port to be mapped [default: 80]
  -h --help                    Show this screen

"""

import os
import subprocess
import sys

try:
    from docopt import docopt
except ImportError:
    print("Please install the python docopt module with 'pip install docopt'")
    sys.exit()


def stop_webserver(args):
    container_name = args['WEBSERVER_NAME']
    cmd = ["docker", "stop", container_name]
    p = subprocess.Popen(cmd)
    p.wait()
    ret_stop = p.returncode

    cmd = ["docker", "rm", container_name]
    p = subprocess.Popen(cmd)
    p.wait()
    ret_rm = p.returncode

    return (ret_stop & ret_rm)


def start_webserver(args):
    nginx_conf_src = os.path.dirname(os.path.realpath(__file__)) + '/nginx.conf'
    nginx_conf_dst = '/etc/nginx/nginx.conf'

    server_root = '/usr/share/nginx/html'

    container_name = args['WEBSERVER_NAME']
    dir_to_serve = os.path.abspath(args['--dir'])
    if not os.path.isdir(dir_to_serve):
	print("ERROR: {} is not a valid directory".format(dir_to_serve))
	return 1
    http_port = args['--port']

    cmd = ["docker",
           "run",
           "--name", container_name,
           "-v", "{0}:{1}:ro".format(nginx_conf_src, nginx_conf_dst),
           "-v", "{0}:{1}:ro".format(dir_to_serve, server_root),
           "-p", "{}:80".format(http_port),
           "-d",
           "nginx"]

    p = subprocess.Popen(cmd)
    p.wait()
    return p.returncode


def main(args):
    if args['start']:
        start_webserver(args)
    elif args['stop']:
        stop_webserver(args)


if __name__ == '__main__':
    args = docopt(__doc__, version=None)
    retcode = main(args)
    sys.exit(retcode)

