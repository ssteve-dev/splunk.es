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
module: splunk_cluster_master_maintenance
short_description: 
description:
  - 
version_added: "1.0"
options:
  maintenance:
    description:
      - 
    required: false
    type: string
    default: 'false'
    choices: [ true, false ]

author: ssteve <https://github.com/ssteve-dev>
"""

EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.six.moves.urllib.error import HTTPError
# Ansible next version
#from ansible_collections.splunk.es.plugins.module_utils.splunk import SplunkRequest
from ansible.module_utils.splunk import SplunkRequest

def main():

    argspec = dict(mode=dict(required=False, type="str", default="false",
                                choices=['true', 'false'])
              )

    module = AnsibleModule(argument_spec=argspec, supports_check_mode=True)

    splunk_request = SplunkRequest(module, headers={"Content-Type": "application/json"})

    request_post_data = {}
    request_post_data['mode'] = module.params['mode']

    try:
        splunk_request.create_update(
                "services/cluster/master/control/default/maintenance", 
                data=urlencode(request_post_data),
        )

        query_dict = splunk_request.get_by_path("services/cluster/master/status")
        
        module.exit_json(changed=True, splunk_cluster_master_maintenace=query_dict["entry"][0]["content"])
    except HTTPError as e:
        # the data monitor doesn't exist
        module.error_json(msg=e)

    #module.exit_json(changed=False, splunk_cluster_master_info=result)

if __name__ == "__main__":
    main()
