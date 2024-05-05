# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from . import githf
import yaml
import ruamel.yaml as ryaml


MACHINE_ORGANIZATION_NAME = 'meta-machina'  # or other organization
PRIVATE_REPO_WITH_TEXT = 'machina'

try:
    gh = githf.connectto_repo(organization=MACHINE_ORGANIZATION_NAME,
                              repository_name=PRIVATE_REPO_WITH_TEXT,
                              private=True)
    MACHINE_YAML = githf.read_file(repository=gh, file_path='machina.yaml')
    META_MACHINA = yaml.load(MACHINE_YAML, Loader=yaml.FullLoader)
except Exception as e:
    machina_path = os.path.join(os.path.dirname(__file__), 'machina.yaml')
    with open(machina_path, 'r') as f:
        META_MACHINA= ryaml.load(f)


if __name__ == '__main__':
    print('You have launched main')

