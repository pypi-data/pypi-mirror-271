# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Licensed under SSPL 1.0, see LICENSE.txt for terms and conditions.
"""

# stdlib
import os
from logging import getLogger
from pathlib import Path

# Behave
from behave.configuration import Configuration # type: ignore
from behave.runner import Runner # type: ignore

# ConfigObj
from configobj import ConfigObj # type: ignore

# ################################################################################################################################
# ################################################################################################################################

if 0:
    from zato.apitest.typing_ import strlistnone # type: ignore

# ################################################################################################################################
# ################################################################################################################################

logger = getLogger('apitest')

# ################################################################################################################################
# ################################################################################################################################

def patch_http_send():

    # stdlib
    import http.client

    # Extract for later use
    orig_send = http.client.HTTPConnection.send # type: ignore

    # This will log data sent
    def _send(self, data): # type: ignore
        logger.info('\n--------- BEGIN Send ---------\n%s\n--------- END Send ---------' % data.decode('utf8'))
        return orig_send(self, data)

    # Patch it now
    http.client.HTTPConnection.send = _send # type: ignore

# ################################################################################################################################
# ################################################################################################################################

def handle(path_:'str', is_verbose:'bool', args:'strlistnone'=None):

    # Local variables
    path = Path(path_) # type: ignore

    # In verbose mode, we need to patch the HTTP library and set a flag that other layers will consult
    if is_verbose:

        # Patch the outgoing connections
        patch_http_send()

        # This needs to be a string
        os.environ['Zato_API_Test_Is_Verbose'] = 'True'

    # If the input is a directory ..
    if path.is_dir():

        # .. it needs to be the top-level one ..
        top_level = path

        # .. and we don't have any specific feature on input ..
        feature_path = None

    # .. otherwise, it's a path to an individual file and we need to find out what its top-level directory with features is
    else:

        # All the elements pointing to the top-level directory ..
        top_level = []

        # .. go through everything we were given on input ..
        for item in path.parts:

            # .. we do not need to go deeper if we are here ..
            if item == 'features':
                break

            # .. otherwise, append it for later use ..
            else:
                top_level.append(item)

        # .. join all the elements found ..
        top_level = os.path.sep.join(top_level)

        # .. on non-Windows, remove initial slash left over from the original path ..
        if top_level.startswith('//'):
            top_level = top_level[1:]

        # .. turn it into a Path object for convenience ..
        top_level = Path(top_level)

        # .. extract the path of the future in relation to the top-level directory ..
        # .. which is what is neede to be given behave on input ..
        feature_path = path.relative_to(top_level)

    # This is resuable
    features_full_path = os.path.join(top_level, 'features')

    file_conf = ConfigObj(os.path.join(features_full_path, 'config.ini'))

    try:
        behave_options = file_conf['behave']['options'] # type: ignore
    except KeyError:
        raise ValueError("Behave config not found. Are you running with the correct path?")
    if args:
        behave_options += ' ' + ' '.join(args)

    tags = os.environ.get('Zato_API_Test_Tags')

    if tags:
        behave_options += ' --tags '
        behave_options += ','.join(tags.split())

    if feature_path:
        behave_options += ' --include '
        behave_options += str(feature_path)

    conf = Configuration(behave_options)
    conf.paths = [features_full_path]
    runner = Runner(conf)
    runner.run()

# ################################################################################################################################
# ################################################################################################################################
