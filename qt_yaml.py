import UI

LOG_LEVEL_NAMES = [
    'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
]
DEFAULT_LOG_LEVEL_NAME = 'INFO'

SETTINGS_YAML_SCHEMA = {
    'master_csv_file': {
        'required': True,
        'type': 'string',
    },
    'block_list_file': {
        'required': True,
        'type': 'string',
    },
    'cache_folder': {
        'required': True,
        'type': 'string',
        },
    'duplicates_list_file': {
        'required': True,
        'type': 'string',
    },
    'log_file': {
        'required': True,  # TODO: allow this to be optional
        'type': 'string',
    },
    'no_scrape': {
        'required': False,  # TODO: we should consider making this CLI only
        'type': 'boolean',
        'default': False,
    },
    'log_level': {
        'required': False,
        'allowed': LOG_LEVEL_NAMES,
        'default': DEFAULT_LOG_LEVEL_NAME,
    },
    'search': {
        'type': 'dict',
        'required': True,
        'schema': {
            'providers': {
                'required': False,
                'allowed': [1,2,3],
                'default': [2,3],
            },
            'locale' : {
                'required': True,
                'allowed': [1,2,3],
            },
            'province_or_state': {'required': True, 'type': 'string'},
            'city': {'required': True, 'type': 'string'},
            'radius': {
                'required': False,
                'type': 'integer',
                'min': 0,
                'default': 25,
            },
            'similar_results': {
                'required': False,
                'type': 'boolean',
                'default': False,
            },
            'keywords': {
                'required': True,
                'type': 'list',
                'schema': {'type': 'string'},
            },
            'max_listing_days': {
                'required': False,
                'type': 'integer',
                'min': 0,
                'default': 20,
            },
            'company_block_list': {
                'required': False,
                'type': 'list',
                'schema': {'type': 'string'},
                'default': ["comp1", "comp2"],
            },
            'remoteness' : {
                'required': False,
                'type': 'string',
                'allowed': ["1", "2"],
                'default': "1",
            }
        },
    },
    'delay': {
        'type': 'dict',
        'required': False,
        'schema' : {
            'algorithm': {
                'required': False,
                'allowed': [1,2, 3],
                'default': 1,
            },
            # TODO: implement custom rule max > min
            'max_duration': {
                'required': False,
                'type': 'float',
                'min': 0,
                'default': 30,
            },
            'min_duration': {
                'required': False,
                'type': 'float',
                'min': 0,
                'default': 5,
            },
            'random': {
                'required': False,
                'type': 'boolean',
                'default': False,
            },
            'converging': {
                'required': False,
                'type': 'boolean',
                'default': False,
            },
        },
    },
    'proxy': {
        'type': 'dict',
        'required': False,
        'schema' : {
            'protocol': {
                'required': False,
                'allowed': ['http', 'https'],
            },
            'ip': {
                'required': False,
                'type': 'ipv4address',
            },
            'port': {
                'required': False,
                'type': 'integer',
                'min': 0,
            },
        },
    },
}

# TODO: Look at the workflow from UI form to CPP file in Qt.

ui_obj = UI.UI()

widget = UI.Widget(class__attr="QMainWindow", name="MainWindow")

ui_obj.set_widget(widget)
ui_obj.export(open("new_file", "w+"), 0)