#!/usr/bin/env python3
"""Auto Updates system and services and projects and Apps"""
__authors__ = [
    "Ryan Bednar <rbed23@gmail.com>"
]

from datetime import datetime
import subprocess
from sys import exit, argv
from typing import Tuple

from config import CONFIGS


def get_ssid() -> bytes:
    # return subprocess.check_output("iwgetid -r")
    return subprocess.check_output("nmcli -t -f NAME connection show --active".split(" "))


def get_subprocess_response(input: str) -> Tuple[str, str]:
    stdin = '' if 'sudo' not in input else CONFIGS['pw']
    popen = subprocess.Popen(input.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = popen.communicate(input=f'{stdin}\n'.encode())
    return stdout, stderr, popen.returncode


def run_command(ip: str) -> str:
    out, err, rc = get_subprocess_response(ip)
    if rc:
        raise ValueError(err)
    return out


def run_apt_updater() -> str:
    return run_command(f"sudo -S apt-get update")


def run_apt_upgrader() -> str:
    return run_command(f"sudo -S apt-get -y upgrade")


def execute_updater(wanted_ssid: str):
    """Execute auto_updater scripting"""
    print(f"-------- Initiating Auto-Updater Script @ {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC --------")

    found_ssid = get_ssid().strip().decode().upper()

    print(f'Looking for [{wanted_ssid.upper()}] SSID...')
    if wanted_ssid.upper() not in found_ssid:
        exit(f'Not on {wanted_ssid.upper()} network.')

    if not (CONFIGS['pw'] and CONFIGS['pw'] != 'abc123'):
        print(f"WARNING: Password [{CONFIGS['pw']}] not configured...")

    try:
        update = run_apt_updater()
    except ValueError as valexc:
        exit(f'ERROR [Updater]: {valexc}')
    else:
        print(update)

    try:
        upgrade = run_apt_upgrader()
    except ValueError as valexc:
        exit(f'ERROR [Upgrader]: {valexc}')
    else:
        print(upgrade)

    print('SUCCESS!')


if __name__ == '__main__':
    try:
        ssid = argv[1]
    except Exception:
        ssid = 'starbucks'
    finally:
        execute_updater(ssid)
