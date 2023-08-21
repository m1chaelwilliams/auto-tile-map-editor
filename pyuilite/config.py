from pyuilite import CONFIG_FILE
import json
import os

data = None
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)

FONT = None
DEFAULTFONTSIZE = 20