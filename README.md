## Directory
servio-backend/
│
├── .env
├── main.py
├── requirements.txt
│
├── data/
│   ├── servio_data.jsonl
│   ├── xml_aspects/
│   └── faiss_index/
│       ├── index.faiss
│       └── index.pkl
│
└── app/
    ├── __init__.py
    │
    ├── core/
    │   ├── __init__.py
    │   └── config.py
    │
    ├── modules/
    │   ├── __init__.py
    │   │
    │   ├── guided/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── routes.py
    │   │   └── service.py
    │   │
    │   ├── direct/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── routes.py
    │   │   └── service.py
    │   │
    │   └── registry_builder/
    │       ├── __init__.py
    │       ├── models.py
    │       ├── routes.py
    │       └── service.py
    │
    └── shared/
        ├── __init__.py
        └── exceptions.py
__________________________________________
## RUN
venv\Scripts\activate  
uvicorn main:app --reload
__________________________________________
## Test Server
GET http://localhost:8000/
{
    "message": "Servio Backend is running"
}
__________________________________________
## Guided Discovery
POST http://localhost:8000/api/guided/recommend
Content-Type: application/json
{
    "query": "I need a scalable API gateway for microservices integration in a cloud environment"
}
{
    "response_text": "Based on the user query, here are the top 5 service recommendations from the registry:\n\n1. **Service Name:** query\n**Confidence:** 60%\n**Brief match explanation:** Although the query service is not specifically designed as an API gateway, it can be used to make calls to the Scaleway API, which is a cloud environment. This service can be used as a starting point for building a custom API gateway.\n\n2. **Service Name:** get_ssh_gateway_config\n**Confidence:** 40%\n**Brief match explanation:** This service returns the ssh_gateway configuration, which might be useful for setting up a cloud environment. However, it's not a direct match for an API gateway.\n\n3. **Service Name:** _associate_eip_with_interface\n**Confidence:** 30%\n**Brief match explanation:** This service is used to associate an elastic IP address with a network interface, which is a task that might be relevant in a cloud environment. However, it's not a direct match for an API gateway.\n\n4. **Service Name:** create_pool\n**Confidence:** 20%\n**Brief match explanation:** This service creates a new node in a pool, which is not directly related to building an API gateway.\n\n5. **Service Name:** _wait_for_spot_instance\n**Confidence:** 10%\n**Brief match explanation:** This service waits for a spot instance request to become active, which is not directly related to building an API gateway.\n\nNote that the confidence scores are subjective and based on the relevance of each service to the user query.",
    "recommendations": [
        {
            "service_name": "query",
            "confidence": 8.5,
            "description": "Make a call to the Scaleway API.",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/cloud/clouds/scaleway.py#L316-L376"
        },
        {
            "service_name": "_wait_for_spot_instance",
            "confidence": 22.5,
            "description": "Helper function that waits for a spot instance request to become active\n    for a specific maximum amount of time.\n\n    :param update_callback: callback function which queries the cloud provider\n                            for spot instance request. It must return None if\n                            the required data, running instance included, is\n                            not available yet.\n    :param update_args: Arguments to pass to update_callback\n    :param update_kwargs: Keyword arguments to pass to update_callback\n    :param timeout: The maximum amount of time(in seconds) to wait for the IP\n                    address.\n    :param interval: The looping interval, i.e., the amount of time to sleep\n                     before the next iteration.\n    :param interval_multiplier: Increase the interval by this multiplier after\n                                each request; helps with throttling\n    :param max_failures: If update_callback returns ``False`` it's considered\n                         query failure. This value is the amount of failures\n                         accepted before giving up.\n    :returns: The update_callback returned data\n    :raises: SaltCloudExecutionTimeout",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/cloud/clouds/ec2.py#L476-L548"
        },
        {
            "service_name": "create_pool",
            "confidence": 22.9,
            "description": "Create a new node if it does not already exist.\n\n    hostname\n        The host/address of the bigip device\n    username\n        The iControl REST username\n    password\n        The iControl REST password\n    name\n        The name of the pool to create\n    members\n        List of members to be added to the pool\n    allow_nat\n        [yes | no]\n    allow_snat\n        [yes | no]\n    description\n        [string]\n    gateway_failsafe_device\n        [string]\n    ignore_persisted_weight\n        [enabled | disabled]\n    ip_tos_to_client\n        [pass-through | [integer]]\n    ip_tos_to_server\n        [pass-through | [integer]]\n    link_qos_to_client\n        [pass-through | [integer]]\n    link_qos_to_server\n        [pass-through | [integer]]\n    load_balancing_mode\n        [dynamic-ratio-member | dynamic-ratio-node |\n        fastest-app-response | fastest-node |\n        least-connections-members |\n        least-connections-node |\n        least-sessions |\n        observed-member | observed-node |\n        predictive-member | predictive-node |\n        ratio-least-connections-member |\n        ratio-least-connections-node |\n        ratio-member | ratio-node | ratio-session |\n        round-robin | weighted-least-connections-member |\n        weighted-least-connections-node]\n    min_active_members\n        [integer]\n    min_up_members\n        [integer]\n    min_up_members_action\n        [failover | reboot | restart-all]\n    min_up_members_checking\n        [enabled | disabled]\n    monitor\n        [name]\n    profiles\n        [none | profile_name]\n    queue_depth_limit\n        [integer]\n    queue_on_connection_limit\n        [enabled | disabled]\n    queue_time_limit\n        [integer]\n    reselect_tries\n        [integer]\n    service_down_action\n        [drop | none | reselect | reset]\n    slow_ramp_time\n        [integer]",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/states/bigip.py#L554-L731"
        },
        {
            "service_name": "get_ssh_gateway_config",
            "confidence": 23.0,
            "description": "Return the ssh_gateway configuration.",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/cloud/clouds/ec2.py#L1053-L1117"
        },
        {
            "service_name": "_associate_eip_with_interface",
            "confidence": 23.1,
            "description": "Accept the id of a network interface, and the id of an elastic ip\n    address, and associate the two of them, such that traffic sent to the\n    elastic ip address will be forwarded (NATted) to this network interface.\n\n    Optionally specify the private (10.x.x.x) IP address that traffic should\n    be NATted to - useful if you have multiple IP addresses assigned to an\n    interface.",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/cloud/clouds/ec2.py#L1599-L1636"
        }
    ]
}
____________________________________
## Aspects Suggestions
GET http://localhost:8000/api/direct/suggest-aspects
Content-Type: application/json
[
    "code",
    "code_tokens",
    "docstring",
    "docstring_tokens",
    "func_name",
    "language",
    "original_string",
    "partition",
    "path",
    "repo",
    "url"
]
__________________________________________
## XML Generation
http://localhost:8000/api/direct/create-xml
Content-Type: application/json
{
    "aspects": [
        {
            "key": "docstring",
            "value": "read"
        },
        {
            "key": "code",
            "value": "write"
        }
    ]
}
{
    "xml_path": "data/xml_aspects\\9c2358ac-1c2a-42b8-a464-386fdf0f8416.xml"
}
__________________________________________
## Direct Discovery
POST http://localhost:8000/api/direct/discover
Content-Type: application/json
Body (JSON):
{
    "query": "create a node",
    "xml_path": "data/xml_aspects/9c2358ac-1c2a-42b8-a464-386fdf0f8416.xml"
}
{
    "matches": [
        {
            "func_name": "install",
            "repo": "saltstack/salt",
            "path": "salt/modules/solarispkg.py",
            "docstring": "Install the passed package. Can install packages from the following\n    sources:\n\n    * Locally (package already exists on the minion\n    * HTTP/HTTPS server\n    * FTP server\n    * Salt master\n\n    Returns a dict containing the new package names and versions:\n\n    .. code-block:: python\n\n        {'<package>': {'old': '<old-version>',\n                       'new': '<new-version>'}}\n\n    CLI Examples:\n\n    .. code-block:: bash\n\n        # Installing a data stream pkg that already exists on the minion\n\n        salt '*' pkg.install sources='[{\"<pkg name>\": \"/dir/on/minion/<pkg filename>\"}]'\n        salt '*' pkg.install sources='[{\"SMClgcc346\": \"/var/spool/pkg/gcc-3.4.6-sol10-sparc-local.pkg\"}]'\n\n        # Installing a data stream pkg that exists on the salt master\n\n        salt '*' pkg.install sources='[{\"<pkg name>\": \"salt://pkgs/<pkg filename>\"}]'\n        salt '*' pkg.install sources='[{\"SMClgcc346\": \"salt://pkgs/gcc-3.4.6-sol10-sparc-local.pkg\"}]'\n\n    CLI Example:\n\n    .. code-block:: bash\n\n        # Installing a data stream pkg that exists on a HTTP server\n        salt '*' pkg.install sources='[{\"<pkg name>\": \"http://packages.server.com/<pkg filename>\"}]'\n        salt '*' pkg.install sources='[{\"SMClgcc346\": \"http://packages.server.com/gcc-3.4.6-sol10-sparc-local.pkg\"}]'\n\n    If working with solaris zones and you want to install a package only in the\n    global zone you can pass 'current_zone_only=True' to salt to have the\n    package only installed in the global zone. (Behind the scenes this is\n    passing '-G' to the pkgadd command.) Solaris default when installing a\n    package in the global zone is to install it in all zones. This overrides\n    that and installs the package only in the global.\n\n    CLI Example:\n\n    .. code-block:: bash\n\n        # Installing a data stream package only in the global zone:\n        salt 'global_zone' pkg.install sources='[{\"SMClgcc346\": \"/var/spool/pkg/gcc-3.4.6-sol10-sparc-local.pkg\"}]' current_zone_only=True\n\n    By default salt automatically provides an adminfile, to automate package\n    installation, with these options set::\n\n        email=\n        instance=quit\n        partial=nocheck\n        runlevel=nocheck\n        idepend=nocheck\n        rdepend=nocheck\n        space=nocheck\n        setuid=nocheck\n        conflict=nocheck\n        action=nocheck\n        basedir=default\n\n    You can override any of these options in two ways. First you can optionally\n    pass any of the options as a kwarg to the module/state to override the\n    default value or you can optionally pass the 'admin_source' option\n    providing your own adminfile to the minions.\n\n    Note: You can find all of the possible options to provide to the adminfile\n    by reading the admin man page:\n\n    .. code-block:: bash\n\n        man -s 4 admin\n\n    CLI Example:\n\n    .. code-block:: bash\n\n        # Overriding the 'instance' adminfile option when calling the module directly\n        salt '*' pkg.install sources='[{\"<pkg name>\": \"salt://pkgs/<pkg filename>\"}]' instance=\"overwrite\"\n\n    SLS Example:\n\n    .. code-block:: yaml\n\n        # Overriding the 'instance' adminfile option when used in a state\n\n        SMClgcc346:\n          pkg.installed:\n            - sources:\n              - SMClgcc346: salt://srv/salt/pkgs/gcc-3.4.6-sol10-sparc-local.pkg\n            - instance: overwrite\n\n    .. note::\n        The ID declaration is ignored, as the package name is read from the\n        ``sources`` parameter.\n\n    CLI Example:\n\n    .. code-block:: bash\n\n        # Providing your own adminfile when calling the module directly\n\n        salt '*' pkg.install sources='[{\"<pkg name>\": \"salt://pkgs/<pkg filename>\"}]' admin_source='salt://pkgs/<adminfile filename>'\n\n        # Providing your own adminfile when using states\n\n        <pkg name>:\n          pkg.installed:\n            - sources:\n              - <pkg name>: salt://pkgs/<pkg filename>\n            - admin_source: salt://pkgs/<adminfile filename>\n\n    .. note::\n        The ID declaration is ignored, as the package name is read from the\n        ``sources`` parameter.",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/modules/solarispkg.py#L201-L385",
            "similarity_score": 2.0
        },
        {
            "func_name": "remove",
            "repo": "saltstack/salt",
            "path": "salt/modules/solarispkg.py",
            "docstring": "Remove packages with pkgrm\n\n    name\n        The name of the package to be deleted\n\n    By default salt automatically provides an adminfile, to automate package\n    removal, with these options set::\n\n        email=\n        instance=quit\n        partial=nocheck\n        runlevel=nocheck\n        idepend=nocheck\n        rdepend=nocheck\n        space=nocheck\n        setuid=nocheck\n        conflict=nocheck\n        action=nocheck\n        basedir=default\n\n    You can override any of these options in two ways. First you can optionally\n    pass any of the options as a kwarg to the module/state to override the\n    default value or you can optionally pass the 'admin_source' option\n    providing your own adminfile to the minions.\n\n    Note: You can find all of the possible options to provide to the adminfile\n    by reading the admin man page:\n\n    .. code-block:: bash\n\n        man -s 4 admin\n\n\n    Multiple Package Options:\n\n    pkgs\n        A list of packages to delete. Must be passed as a python list. The\n        ``name`` parameter will be ignored if this option is passed.\n\n    .. versionadded:: 0.16.0\n\n\n    Returns a dict containing the changes.\n\n    CLI Example:\n\n    .. code-block:: bash\n\n        salt '*' pkg.remove <package name>\n        salt '*' pkg.remove SUNWgit\n        salt '*' pkg.remove <package1>,<package2>,<package3>\n        salt '*' pkg.remove pkgs='[\"foo\", \"bar\"]'",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/modules/solarispkg.py#L388-L488",
            "similarity_score": 2.0
        },
        {
            "func_name": "interfaces",
            "repo": "saltstack/salt",
            "path": "salt/modules/sysfs.py",
            "docstring": "Generate a dictionary with all available interfaces relative to root.\n    Symlinks are not followed.\n\n    CLI example:\n     .. code-block:: bash\n\n        salt '*' sysfs.interfaces block/bcache0/bcache\n\n    Output example:\n     .. code-block:: json\n\n       {\n          \"r\": [\n            \"state\",\n            \"partial_stripes_expensive\",\n            \"writeback_rate_debug\",\n            \"stripe_size\",\n            \"dirty_data\",\n            \"stats_total/cache_hits\",\n            \"stats_total/cache_bypass_misses\",\n            \"stats_total/bypassed\",\n            \"stats_total/cache_readaheads\",\n            \"stats_total/cache_hit_ratio\",\n            \"stats_total/cache_miss_collisions\",\n            \"stats_total/cache_misses\",\n            \"stats_total/cache_bypass_hits\",\n          ],\n          \"rw\": [\n            \"writeback_rate\",\n            \"writeback_rate_update_seconds\",\n            \"cache_mode\",\n            \"writeback_delay\",\n            \"label\",\n            \"writeback_running\",\n            \"writeback_metadata\",\n            \"running\",\n            \"writeback_rate_p_term_inverse\",\n            \"sequential_cutoff\",\n            \"writeback_percent\",\n            \"writeback_rate_d_term\",\n            \"readahead\"\n          ],\n          \"w\": [\n            \"stop\",\n            \"clear_stats\",\n            \"attach\",\n            \"detach\"\n          ]\n       }\n\n    .. note::\n      * 'r' interfaces are read-only\n      * 'w' interfaces are write-only (e.g. actions)\n      * 'rw' are interfaces that can both be read or written",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/modules/sysfs.py#L170-L263",
            "similarity_score": 2.0
        },
        {
            "func_name": "gen_accept",
            "repo": "saltstack/salt",
            "path": "salt/wheel/key.py",
            "docstring": "r'''\n    Generate a key pair then accept the public key. This function returns the\n    key pair in a dict, only the public key is preserved on the master. Returns\n    a dictionary.\n\n    id\\_\n        The name of the minion for which to generate a key pair.\n\n    keysize\n        The size of the key pair to generate. The size must be ``2048``, which\n        is the default, or greater. If set to a value less than ``2048``, the\n        key size will be rounded up to ``2048``.\n\n    force\n        If a public key has already been accepted for the given minion on the\n        master, then the gen_accept function will return an empty dictionary\n        and not create a new key. This is the default behavior. If ``force``\n        is set to ``True``, then the minion's previously accepted key will be\n        overwritten.\n\n    .. code-block:: python\n\n        >>> wheel.cmd('key.gen_accept', ['foo'])\n        {'pub': '-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBC\n        ...\n        BBPfamX9gGPQTpN9e8HwcZjXQnmg8OrcUl10WHw09SDWLOlnW+ueTWugEQpPt\\niQIDAQAB\\n\n        -----END PUBLIC KEY-----',\n        'priv': '-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEA42Kf+w9XeZWgguzv\n        ...\n        QH3/W74X1+WTBlx4R2KGLYBiH+bCCFEQ/Zvcu4Xp4bIOPtRKozEQ==\\n\n        -----END RSA PRIVATE KEY-----'}\n\n    We can now see that the ``foo`` minion's key has been accepted by the master:\n\n    .. code-block:: python\n\n        >>> wheel.cmd('key.list', ['accepted'])\n        {'minions': ['foo', 'minion1', 'minion2', 'minion3']}",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/wheel/key.py#L374-L421",
            "similarity_score": 2.0
        },
        {
            "func_name": "Minion._thread_return",
            "repo": "saltstack/salt",
            "path": "salt/minion.py",
            "docstring": "This method should be used as a threading target, start the actual\n        minion side execution.",
            "url": "https://github.com/saltstack/salt/blob/e8541fd6e744ab0df786c0f76102e41631f45d46/salt/minion.py#L1631-L1851",
            "similarity_score": 2.0
        }
    ]
}
__________________________________________
## Build Registery
POST http://localhost:8000/api/registry_builder/build
Content-Type: application/json
{
  "query": "microservice language:python",
?  "limit": 5
}
{
    "success": true,
    "message": "Registry built successfully",
    "filename": "registry_1.json",
    "repositories": [
        {
            "name": "serve",
            "full_name": "jina-ai/serve",
            "description": "☁️ Build multimodal AI applications with cloud-native stack",
            "url": "https://github.com/jina-ai/serve",
            "stars": 21513,
            "forks": 2222,
            "language": "Python",
            "license": "Apache License 2.0",
            "readme": null
        },
        {
            "name": "falcon",
            "full_name": "falconry/falcon",
            "description": "The no-magic web API and microservices framework for Python developers, with an emphasis on reliability and performance at scale.",
            "url": "https://github.com/falconry/falcon",
            "stars": 9631,
            "forks": 953,
            "language": "Python",
            "license": "Apache License 2.0",
            "readme": null
        },
        {
            "name": "nameko",
            "full_name": "nameko/nameko",
            "description": "Python framework for building microservices",
            "url": "https://github.com/nameko/nameko",
            "stars": 4729,
            "forks": 470,
            "language": "Python",
            "license": "Apache License 2.0",
            "readme": null
        },
        {
            "name": "emissary",
            "full_name": "emissary-ingress/emissary",
            "description": "open source Kubernetes-native API gateway for microservices built on the Envoy Proxy",
            "url": "https://github.com/emissary-ingress/emissary",
            "stars": 4423,
            "forks": 688,
            "language": "Python",
            "license": "Apache License 2.0",
            "readme": null
        },
        {
            "name": "microservices-demo",
            "full_name": "microservices-demo/microservices-demo",
            "description": "Deployment scripts & config for Sock Shop",
            "url": "https://github.com/microservices-demo/microservices-demo",
            "stars": 3681,
            "forks": 2859,
            "language": "Python",
            "license": "Apache License 2.0",
            "readme": null
        }
    ]
}