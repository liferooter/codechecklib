import math
from datetime import time, datetime
from typing import List


def get_sandbox_command(has_internet: bool, blacklist_dirs: List[str], real_command: List[str] or str,
                        available_binaries: List[str], return_list: bool, timeout: int = None,
                        cgroup: str = None, user: str = None):
    command = 'firejail --private-dev --shell=none --seccomp --quiet --caps --noroot'
    blacklist_dirs = blacklist_dirs.copy()
    if user:
        command = 'sudo -u ' + user + ' ' + command
    else:
        command += ' --private'
    if not has_internet:
        command += ' --net=none'
    if timeout:
        timeout = time.strftime(datetime.utcfromtimestamp(math.ceil(timeout / 1000)).time(), '%H:%M:%S')
        command += ' --timeout=' + timeout
    blacklist_dirs.append('/sys/fs/cgroup')
    for i in blacklist_dirs:
        command += f' --blacklist={i}'
    if available_binaries:
        command += f' --private-bin=' + ','.join(available_binaries)
    if cgroup:
        command += f' --cgroup=/sys/fs/cgroup/memory/{cgroup}/tasks'
    command += ' env -i LC_ALL=en_US.UTF-8 PATH=/bin:/usr/bin:/usr/local/bin '
    if isinstance(real_command, list):
        command += ' '.join(real_command)
    else:
        command += real_command
    if return_list:
        return command.split(' ')
    return command
