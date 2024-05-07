#!/usr/bin/env python
#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import os
import argparse

from sciveo.common.tools.logger import *
from sciveo.monitoring.start import MonitorStart
from sciveo.common.tools.configuration import GlobalConfiguration


def main():
  config = GlobalConfiguration.get()

  parser = argparse.ArgumentParser(description='sciveo CLI')
  parser.add_argument('command', choices=['monitor', 'net'], help='Command to execute')
  parser.add_argument('--period', type=int, default=120, help='Period in seconds')
  parser.add_argument('--block', type=bool, default=True, help='Block flag')
  parser.add_argument('--auth', type=str, default=config['secret_access_key'], help='Auth secret access key')
  args = parser.parse_args()

  if args.command == 'monitor':
    MonitorStart(period=args.period, block=args.block)()
  elif args.command == 'net':
    warning(args.command, "not implemented")
  else:
    warning(args.command, "not implemented")

if __name__ == '__main__':
    main()