"""Ansible Vars Plugin for Local Variables"""

# Copyright: 2019 Freek Dijkstra <freek@macfreek.nl>
# Licence: MIT license

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type  # pylint: disable=invalid-name

import os
import socket
from ansible.plugins.vars import BaseVarsPlugin
from ansible.utils.vars import combine_vars
from ansible.errors import AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native, to_text

DOCUMENTATION = '''
    vars: local_vars
    short_description: Load variables from file based on local hostname`.
    description:
        - Ansibe plugin
        - Loads YAML vars from `local_vars/<local hostname> files`.
        - Files are restricted by extension to one of .yaml, .json, .yml or no extension.
        - Hidden (starting with '.') and backup (ending with '~') files and directories are ignored.
        - Useful if you have multiple Ansible controllers with minimal differences.
        - Install this plugin in <your Ansible directory>/vars_plugins/local_vars.py
'''


# pylint: disable=R0903
class VarsModule(BaseVarsPlugin):
    """
    Ansible Vars Plugin for Local Variables
    
    short_description: Load variables from file based on local hostname`.
    description:
        - Sets `local_hostname` variable.
        - Loads YAML vars from `local_vars/<local hostname> files`.
        - Files are restricted by extension to one of .yaml, .json, .yml or no extension.
        - Hidden (starting with '.') and backup (ending with '~') files and directories are ignored.
        - Useful if you have multiple Ansible controllers with minimal differences.
    options:
        - hostname:
            description: hostname for which to load variables.
            required: false
            default: output of hostname(1)
    """

    def get_vars(self, loader, path, entities):
        """Entry point called from Ansible to get vars."""

        super(VarsModule, self).get_vars(loader, path, entities)

        try:
            # TODO: first check hostname variable. This is useful to override hostname on the command line with the -e option.
            hostname = socket.gethostname()
            data = { "local_hostname": hostname }

            found_files = []
            # load vars
            b_opath = os.path.realpath(to_bytes(os.path.join(self._basedir, 'local_vars')))
            opath = to_text(b_opath)

            found_files = loader.find_vars_files(opath, hostname)
            for found in found_files:
                self._display.debug("\tprocessing file %s" % found)
                new_data = loader.load_from_file(found, cache=True, unsafe=True)
                if new_data:  # ignore empty files
                    data = combine_vars(data, new_data)

        except Exception as e:
            raise AnsibleParserError(to_native(e))
        return data
