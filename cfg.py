'''
Date: 2021-03-26 19:20:38
LastEditors: LIULIJING
LastEditTime: 2021-03-26 19:42:11
'''
import json
import json.decoder

Conf = dict()
class ModisNsidcSpiderConfig:
    def __init__(self, config_file='configuration.json'):
        super().__init__()
        with open(config_file) as f:
            Conf = json.load(f)

