## Directory
servio-backend/
│
├── .env
├── main.py
├── requirements.txt
│
├── data/
│   ├── servio_data.jsonl
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
## Test Guided
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
__________________________________________

