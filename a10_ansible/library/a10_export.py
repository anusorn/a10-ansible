#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_export
description:
    - None
short_description: Configures A10 export
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
    geo_location:
        description:
        - "None"
        required: False
    ssl_cert_key:
        description:
        - "None"
        required: False
    bw_list:
        description:
        - "None"
        required: False
    lw_4o6:
        description:
        - "None"
        required: False
    tgz:
        description:
        - "None"
        required: False
    merged_pcap:
        description:
        - "None"
        required: False
    syslog:
        description:
        - "None"
        required: False
    use_mgmt_port:
        description:
        - "None"
        required: False
    auth_portal:
        description:
        - "None"
        required: False
    fixed_nat_archive:
        description:
        - "None"
        required: False
    aflex:
        description:
        - "None"
        required: False
    fixed_nat:
        description:
        - "None"
        required: False
    saml_idp_name:
        description:
        - "None"
        required: False
    thales_kmdata:
        description:
        - "None"
        required: False
    per_cpu:
        description:
        - "None"
        required: False
    debug_monitor:
        description:
        - "None"
        required: False
    policy:
        description:
        - "None"
        required: False
    lw_4o6_binding_table_validation_log:
        description:
        - "None"
        required: False
    thales_secworld:
        description:
        - "None"
        required: False
    csr:
        description:
        - "None"
        required: False
    auth_portal_image:
        description:
        - "None"
        required: False
    ssl_crl:
        description:
        - "None"
        required: False
    class_list:
        description:
        - "None"
        required: False
    status_check:
        description:
        - "None"
        required: False
    dnssec_ds:
        description:
        - "None"
        required: False
    profile:
        description:
        - "None"
        required: False
    local_uri_file:
        description:
        - "None"
        required: False
    wsdl:
        description:
        - "None"
        required: False
    ssl_key:
        description:
        - "None"
        required: False
    store:
        description:
        - "Field store"
        required: False
        suboptions:
            create:
                description:
                - "None"
            name:
                description:
                - "None"
            remote_file:
                description:
                - "Field remote_file"
            delete:
                description:
                - "None"
    externalfilename:
        description:
        - "None"
        required: False
    remote_file:
        description:
        - "None"
        required: False
    store_name:
        description:
        - "None"
        required: False
    ca_cert:
        description:
        - "None"
        required: False
    axdebug:
        description:
        - "None"
        required: False
    running_config:
        description:
        - "None"
        required: False
    xml_schema:
        description:
        - "None"
        required: False
    startup_config:
        description:
        - "None"
        required: False
    ssl_cert:
        description:
        - "None"
        required: False
    dnssec_dnskey:
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
AVAILABLE_PROPERTIES = ["aflex","auth_portal","auth_portal_image","axdebug","bw_list","ca_cert","class_list","csr","debug_monitor","dnssec_dnskey","dnssec_ds","externalfilename","fixed_nat","fixed_nat_archive","geo_location","local_uri_file","lw_4o6","lw_4o6_binding_table_validation_log","merged_pcap","per_cpu","policy","profile","remote_file","running_config","saml_idp_name","ssl_cert","ssl_cert_key","ssl_crl","ssl_key","startup_config","status_check","store","store_name","syslog","tgz","thales_kmdata","thales_secworld","use_mgmt_port","wsdl","xml_schema",]

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
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        geo_location=dict(type='str',),
        ssl_cert_key=dict(type='str',),
        bw_list=dict(type='str',),
        lw_4o6=dict(type='str',),
        tgz=dict(type='bool',),
        merged_pcap=dict(type='bool',),
        syslog=dict(type='str',),
        use_mgmt_port=dict(type='bool',),
        auth_portal=dict(type='str',),
        fixed_nat_archive=dict(type='str',),
        aflex=dict(type='str',),
        fixed_nat=dict(type='str',),
        saml_idp_name=dict(type='str',),
        thales_kmdata=dict(type='str',),
        per_cpu=dict(type='bool',),
        debug_monitor=dict(type='str',),
        policy=dict(type='str',),
        lw_4o6_binding_table_validation_log=dict(type='str',),
        thales_secworld=dict(type='str',),
        csr=dict(type='str',),
        auth_portal_image=dict(type='str',),
        ssl_crl=dict(type='str',),
        class_list=dict(type='str',),
        status_check=dict(type='bool',),
        dnssec_ds=dict(type='str',),
        profile=dict(type='str',),
        local_uri_file=dict(type='str',),
        wsdl=dict(type='str',),
        ssl_key=dict(type='str',),
        store=dict(type='dict',create=dict(type='bool',),name=dict(type='str',),remote_file=dict(type='str',),delete=dict(type='bool',)),
        externalfilename=dict(type='str',),
        remote_file=dict(type='str',),
        store_name=dict(type='str',),
        ca_cert=dict(type='str',),
        axdebug=dict(type='str',),
        running_config=dict(type='bool',),
        xml_schema=dict(type='str',),
        startup_config=dict(type='bool',),
        ssl_cert=dict(type='str',),
        dnssec_dnskey=dict(type='str',)
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/export"
    f_dict = {}

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/export"
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
    payload = build_json("export", module)
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
    payload = build_json("export", module)
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
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
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