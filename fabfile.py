import os
from fabric.api import local, env, run, cd, sudo, prefix, settings, execute, task, put
from fabric.contrib.files import exists
from contextlib import contextmanager

env.hosts = ['root@pocupine.ddns.net:38889']


def host_type():
    run('uname -s')


def diskspace():
    run('df')


def check():
    # check host type
    host_type()

    # Check diskspace
    diskspace()