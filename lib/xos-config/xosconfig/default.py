DEFAULT_VALUES = {
    'xos_dir': '/opt/xos',
    'logging': {
        'level': 'info',
        'channels': ['file', 'console'],
        'logstash_hostport': 'cordloghost:5617'
    },
    'accessor': {
        'endpoint': 'xos-core.cord.lab:50051',
    },
    'keep_temp_files': False,
    'enable_watchers': False,
    'dependency_graph': '/opt/xos/model-deps',
    'error_map_path': '/opt/xos/error_map.txt',
    'feefie': {
        'client_user': 'pl'
    },
    'proxy_ssh': {
      'enabled': True,
      'key': '/opt/cord_profile/node_key',
      'user': 'root'
    },
    'node_key': '/opt/cord_profile/node_key',
    'config_dir': '/etc/xos/sync',
    'backoff_disabled': True
}