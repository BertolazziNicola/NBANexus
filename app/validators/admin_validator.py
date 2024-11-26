from cerberus import Validator
        
def validate_login(data):
    schema = {
        'email': {
            'type': 'string',
            'required': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'remember': {
            'type': 'boolean',
            'required': False,
            'default': False,
        },
    }
    
    v = Validator(schema)
    if v.validate(data):
        return v.document, None
    else:
        return None, v.errors
    
def validate_profile(data):
    schema = {
        'password': {
            'type': 'string',
            'required': True,
        },
        'new-password': {
            'type': 'string',
            'required': True,
            'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{7,45}$',
        },
    }
    
    v = Validator(schema)
    if v.validate(data):
        return v.document, None
    else:
        return None, v.errors
    
def validate_create_user(data):
    schema = {
        'email': {
            'type': 'string',
            'required': True,
            'regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        },
        'password': {
            'type': 'string',
            'required': True,
            'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{7,45}$',
        },
        're-password': {
            'type': 'string',
            'required': False,
        },
        'role': {
            'type': 'string',
            'required': True,
            'allowed': ['Admin'],  # Allow only 'admin'
        },
    }
    
    v = Validator(schema)
    if v.validate(data):
        return v.document, None
    else:
        return None, v.errors
    
def validate_modify_user(data):
    schema = {
        '_id': {
            'type': 'string',
            'required': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'new-password': {
            'type': 'string',
            'required': True,
            'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{7,45}$',
        },
    }
    
    v = Validator(schema)
    if v.validate(data):
        return v.document, None
    else:
        return None, v.errors