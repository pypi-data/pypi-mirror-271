'''
Created on 30 Apr 2024

@author: jacklok
'''
from functools import wraps
from flask import request
import logging,json
from flask.globals import session

logger = logging.getLogger('debug')

def request_json(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_json = request.get_json()
        
        request_json = json.loads(json.dumps({**request_json}))
            
        return f(*args, request_json, **kwargs)

    return decorated_function

def request_headers(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = request.headers
        logger.debug('headers before=%s', headers)
        headers = json.loads(json.dumps({**headers}))
        logger.debug('headers after=%s', headers)
        headers = dict((k.lower(), v) for k, v in headers.items())    
        
        return f(*args, headers, **kwargs)

    return decorated_function

def request_args(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        values = {}
        values.update(request.args)
        
        return f(*args, values, **kwargs)

    return decorated_function

def request_values(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        values = {}
        values.update(request.args)
        values.update(request.form)
        
        request_json = request.get_json()
        
        request_json = json.loads(json.dumps({**request_json}))
        
        values.update(request_json)
        
        return f(*args, values, **kwargs)

    return decorated_function

def request_form(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        return f(*args, request.form, **kwargs)

    return decorated_function

def session_value(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        return f(*args, session, **kwargs)

    return decorated_function
