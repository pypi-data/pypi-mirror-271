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
import threading


class GlobalConfiguration:
  config = None
  lock_config = threading.Lock()

  def __init__(self) -> None:
    home = os.path.expanduser('~')
    self.base_path = os.path.join(home, '.sciveo')
    self.data = {}

    self.default = {
      "api_base_url": "https://sciveo.com",
      "log_min_level": "DEBUG"
    }

    try:
      self.read_local_files()
      self.read_environment()
    except Exception as e:
      error(type(self).__name__, "Exception", e)

  @staticmethod
  def get():
    with GlobalConfiguration.lock_config:
      if GlobalConfiguration.config is None:
        GlobalConfiguration.config = GlobalConfiguration()
      return GlobalConfiguration.config

  def __getitem__(self, key):
    key = key.lower()
    return self.data.get(key, self.default.get(key, ""))

  def read_environment(self):
    for k, v in os.environ.items():
      k = k.lower()
      if k.startswith("sciveo_"):
        k = k.replace("sciveo_", "")
        self.data[k] = v

  def read_local_files(self):
    if os.path.exists(self.base_path):
      for path, _, files in os.walk(self.base_path):
        for file_name in files:
          with open(os.path.join(path, file_name), 'r') as fp:
            lines = fp.readlines()
            for line in lines:
              parts = line.strip().split('=')
              if len(parts) == 2:
                key = parts[0].strip().lower().replace("sciveo_", "")
                value = parts[1].strip()
                self.data[key] = value
