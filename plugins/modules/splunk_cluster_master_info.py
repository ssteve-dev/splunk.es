#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
}


DOCUMENTATION = """
---
module: splunk_cluster_master_info
short_description: Informations/status from a Splunk Cluster Master
description:
  - This module allows to get informations and/or status from a Splunk Cluster Master, peers or indexes
version_added: "1.0"
options:
  action:
    description:
      - To get informations, status from a Splunk Cluster Master, peers or indexes
    required: false
    type: str
    default: 'status'
    choices: [ status, health, info, indexes, peers ]

author: ssteve <https://github.com/ssteve-dev>
"""

EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.six.moves.urllib.error import HTTPError
# Ansible next version
#from ansible_collections.splunk.es.plugins.module_utils.splunk import SplunkRequest
from ansible.module_utils.splunk import SplunkRequest

def main():

    argspec = dict(action=dict(required=False, type="str", default="status",
                                choices=['status', 'health', 'info', 'indexes', 'peers'])
              )

    module = AnsibleModule(argument_spec=argspec, supports_check_mode=True)

    splunk_request = SplunkRequest(module, headers={"Content-Type": "application/json"})

    action = module.params['action']

    try:
        query_dict = splunk_request.get_by_path("services/cluster/master/" + action)
    except HTTPError as e:
        # the data monitor doesn't exist
        module.error_json(msg=e)

    if len(query_dict["entry"]) > 0:
        result = query_dict["entry"][0]["content"]
    else:
        result = "No result"
    
    module.exit_json(changed=False, splunk_cluster_master_info=result)

if __name__ == "__main__":
    main()
