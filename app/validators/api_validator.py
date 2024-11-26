from cerberus import Validator

def validate_import_players(data):
    schema = {
        'season': {
            'type': 'string',
            'required': True,
            'regex': r'^\d{4}-\d{2}$',  # Regular expression for the format YYYY-YY
        },
        'overwrite': {
            'type': 'boolean',
            'required': False,
            'default': True,
        }
    }
    
    v = Validator(schema)
    if v.validate(data):
        return v.document, None
    else:
        return None, v.errors
    
def validate_import_teams(data):
    schema = {
        'save-images': {
            'type': 'boolean',
            'required': False,
            'default': False,
        },
        'overwrite': {
            'type': 'boolean',
            'required': False,
            'default': False,
        }
    }
    
    v = Validator(schema)
    if v.validate(data):
        return v.document, None
    else:
        return None, v.errors
