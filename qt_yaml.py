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


def __add_form_label_row(label: str, grid_layout: UI.Layout, row):
    """
    Adds a label and a QLineEdit on the same row of grid_layout
    :param label:
    :param grid_layout:
    :param row:
    :return:
    """
    label_wdget = UI.Widget(class__attr="QLabel", name="setting")
    label_property = UI.Property()
    label_property.set_name("text")
    text_label = UI.String()
    text_label.set_valueOf_(label)
    label_property.set_string(text_label)
    label_wdget.add_property(label_property)

    text_edit = UI.Widget(class__attr="QLineEdit", name="edit_setting_" + label)

    grid_layout.add_item(UI.LayoutItem(row=row, column=0, widget=label_wdget))
    grid_layout.add_item(UI.LayoutItem(row=row, column=1, widget=text_edit))

def __add_form_boolean_row(label: str, grid_layout: UI.Layout, row, checked: bool = False):
    """
    Adds a label and a QLineEdit on the same row of grid_layout
    :param label:
    :param grid_layout:
    :param row:
    :return:
    """
    label_wdget = UI.Widget(class__attr="QLabel", name="setting")
    label_property = UI.Property()
    label_property.set_name("text")
    text_label = UI.String()
    text_label.set_valueOf_(label)
    label_property.set_string(text_label)
    label_wdget.add_property(label_property)

    checkbox_text_label = UI.String()
    checkbox_text_label.set_valueOf_(label + "_check")
    checkbox_label_property = UI.Property()
    checkbox_label_property.set_name("text")
    checkbox_label_property.set_string(checkbox_text_label)

    check_box = UI.Widget(class__attr="QCheckBox", name="edit_setting_" + label)

    checked_property = UI.Property(bool=str(checked).lower())
    check_box.add_property(checked_property)
    check_box.add_property(checkbox_label_property)

    grid_layout.add_item(UI.LayoutItem(row=row, column=0, widget=label_wdget))
    grid_layout.add_item(UI.LayoutItem(row=row, column=1, widget=check_box))

def from_schema_to_widget(schema: dict):
    widget_container = UI.Widget(class__attr="QWidget", name="YAMLForm")
    rect_property = UI.Property()
    rect_property.set_name("geometry")
    rect_property.set_rect(UI.Rect(width=400, height=400, x=0, y=0))
    widget_container.add_property(rect_property)
    layout = UI.Layout(class_="QGridLayout", name="gridLayout")
    current_row = 0
    for setting in schema:
        setting_node = schema[setting]
        if 'type' in setting_node and \
                setting_node['type'] == 'string':
            __add_form_label_row(setting, layout, current_row)

        elif 'type' in setting_node and \
                setting_node['type'] == 'boolean':
            __add_form_boolean_row(setting, layout, current_row)

        current_row += 1
    widget_container.set_layout([layout])

    return widget_container

ui_obj = UI.UI(version="4.0", class_="YAMLForm")

form = from_schema_to_widget(SETTINGS_YAML_SCHEMA)
ui_obj.set_widget(form)


# ui_obj.set_class()

ui_obj.export(open("new_file.xml", "w+"), 0, name_='ui')
# widget = UI.Widget(class__attr="QMainWindow", name="MainWindow")

# ui_obj.set_widget(widget)

# ui_obj.export(open("new_file", "w+"), 0)