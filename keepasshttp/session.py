import logging
import os
import yaml

import xdg.BaseDirectory

from keepasshttp import protocol


logger = logging.getLogger(__name__)


class Session(object):
    def __init__(self, key, id_):
        self.key = key
        self.id_ = id_

    @classmethod
    def start(cls, app_name):
        config_dir = xdg.BaseDirectory.save_config_path(app_name)
        config_path = os.path.join(config_dir, 'keepasshttp.yml')
        if os.path.exists(config_path):
            with open(config_path) as fin:
                config = yaml.safe_load(fin)
            id_ = config['id']
            key = config['key']
            if not protocol.testAssociate(id_, key):
                logger.warning("Previous association failed. Loading new association")
                key, id_ = getAndSaveNewAssociation(config_path)
        else:
            logger.info("No previous association. Loading new association")
            key, id_ = getAndSaveNewAssociation(config_path)
        return cls(key, id_)

    def getLogins(self, url):
        return protocol.getLogins(url, self.id_, self.key)


def getAndSaveNewAssociation(config_path):
    key, id_ = protocol.associate()
    with open(config_path, 'w') as fout:
        fout.write(yaml.safe_dump({'key': key, 'id': id_}, default_flow_style=False))
    return key, id_
