#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_route_map_set
description:
    - None
short_description: Configures A10 route.map.set
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    extcommunity:
        description:
        - "Field extcommunity"
        required: False
        suboptions:
            rt:
                description:
                - "Field rt"
            soo:
                description:
                - "Field soo"
    origin:
        description:
        - "Field origin"
        required: False
        suboptions:
            egp:
                description:
                - "None"
            incomplete:
                description:
                - "None"
            igp:
                description:
                - "None"
    originator_id:
        description:
        - "Field originator_id"
        required: False
        suboptions:
            originator_ip:
                description:
                - "None"
    weight:
        description:
        - "Field weight"
        required: False
        suboptions:
            weight_val:
                description:
                - "None"
    level:
        description:
        - "Field level"
        required: False
        suboptions:
            value:
                description:
                - "None"
    ip:
        description:
        - "Field ip"
        required: False
        suboptions:
            next_hop:
                description:
                - "Field next_hop"
    metric:
        description:
        - "Field metric"
        required: False
        suboptions:
            value:
                description:
                - "None"
    as_path:
        description:
        - "Field as_path"
        required: False
        suboptions:
            num:
                description:
                - "None"
            num2:
                description:
                - "None"
            prepend:
                description:
                - "None"
    comm_list:
        description:
        - "Field comm_list"
        required: False
        suboptions:
            name:
                description:
                - "None"
            v_std:
                description:
                - "None"
            v_exp_delete:
                description:
                - "None"
            v_exp:
                description:
                - "None"
            name_delete:
                description:
                - "None"
            delete:
                description:
                - "None"
    atomic_aggregate:
        description:
        - "None"
        required: False
    community:
        description:
        - "None"
        required: False
    local_preference:
        description:
        - "Field local_preference"
        required: False
        suboptions:
            val:
                description:
                - "None"
    ddos:
        description:
        - "Field ddos"
        required: False
        suboptions:
            class_list_name:
                description:
                - "None"
            class_list_cid:
                description:
                - "None"
            zone:
                description:
                - "None"
    tag:
        description:
        - "Field tag"
        required: False
        suboptions:
            value:
                description:
                - "None"
    aggregator:
        description:
        - "Field aggregator"
        required: False
        suboptions:
            aggregator_as:
                description:
                - "Field aggregator_as"
    dampening_cfg:
        description:
        - "Field dampening_cfg"
        required: False
        suboptions:
            dampening_max_supress:
                description:
                - "None"
            dampening:
                description:
                - "None"
            dampening_penalty:
                description:
                - "None"
            dampening_half_time:
                description:
                - "None"
            dampening_supress:
                description:
                - "None"
            dampening_reuse:
                description:
                - "None"
    ipv6:
        description:
        - "Field ipv6"
        required: False
        suboptions:
            next_hop_1:
                description:
                - "Field next_hop_1"
    metric_type:
        description:
        - "Field metric_type"
        required: False
        suboptions:
            value:
                description:
                - "None"
    uuid:
        description:
        - "None"
        required: False


"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["aggregator","as_path","atomic_aggregate","comm_list","community","dampening_cfg","ddos","extcommunity","ip","ipv6","level","local_preference","metric","metric_type","origin","originator_id","tag","uuid","weight",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory, session_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        a10_port=dict(type='int', required=True),
        a10_protocol=dict(type='str', choices=["http", "https"]),
        state=dict(type='str', default="present", choices=["present", "absent"]),
        partition=dict(type='str', required=False)
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        extcommunity=dict(type='dict',rt=dict(type='dict',value=dict(type='str',)),soo=dict(type='dict',value=dict(type='str',))),
        origin=dict(type='dict',egp=dict(type='bool',),incomplete=dict(type='bool',),igp=dict(type='bool',)),
        originator_id=dict(type='dict',originator_ip=dict(type='str',)),
        weight=dict(type='dict',weight_val=dict(type='int',)),
        level=dict(type='dict',value=dict(type='str',choices=['level-1','level-1-2','level-2'])),
        ip=dict(type='dict',next_hop=dict(type='dict',address=dict(type='str',))),
        metric=dict(type='dict',value=dict(type='str',)),
        as_path=dict(type='dict',num=dict(type='int',),num2=dict(type='int',),prepend=dict(type='str',)),
        comm_list=dict(type='dict',name=dict(type='str',),v_std=dict(type='int',),v_exp_delete=dict(type='bool',),v_exp=dict(type='int',),name_delete=dict(type='bool',),delete=dict(type='bool',)),
        atomic_aggregate=dict(type='bool',),
        community=dict(type='str',),
        local_preference=dict(type='dict',val=dict(type='int',)),
        ddos=dict(type='dict',class_list_name=dict(type='str',),class_list_cid=dict(type='int',),zone=dict(type='str',)),
        tag=dict(type='dict',value=dict(type='int',)),
        aggregator=dict(type='dict',aggregator_as=dict(type='dict',ip=dict(type='str',),asn=dict(type='int',))),
        dampening_cfg=dict(type='dict',dampening_max_supress=dict(type='int',),dampening=dict(type='bool',),dampening_penalty=dict(type='int',),dampening_half_time=dict(type='int',),dampening_supress=dict(type='int',),dampening_reuse=dict(type='int',)),
        ipv6=dict(type='dict',next_hop_1=dict(type='dict',local=dict(type='dict',address=dict(type='str',)),address=dict(type='str',))),
        metric_type=dict(type='dict',value=dict(type='str',choices=['external','internal','type-1','type-2'])),
        uuid=dict(type='str',)
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/route-map/{tag}+{action}+{sequence}/set"
    f_dict = {}

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/route-map/{tag}+{action}+{sequence}/set"
    f_dict = {}

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        if isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            if isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def get(module):
    return module.client.get(existing_url(module))

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("set", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result, existing_config):
    payload = build_json("set", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result, existing_config):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result, existing_config)

def absent(module, result):
    return delete(module, result)

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    partition = module.params["partition"]

    # TODO(remove hardcoded port #)
    a10_port = module.params["a10_port"] 
    a10_protocol = module.params["a10_protocol"]

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
    if partition:
        module.client.activate_partition(partition)

    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)
        module.client.session.close()
    elif state == 'absent':
        result = absent(module, result)
        module.client.session.close()
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()