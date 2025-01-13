#############################################
#                                           #
#             Decorator Module              #
#                                           #
#  Author: Shan                             #
#                                           #
#############################################


# Importing necessary libraries #################

from flask import redirect, url_for,session,request
from functools import wraps
from .permissions import perm

#################################################


# Functions #####################################

# Is logged in
def is_authenticated():
    username = session.get('username')
    return username and len(username.strip()) > 0

# Is logged out
def is_not_authenticated():
    username = session.get('username')
    return username==None

# Have permission
def have_permissions():
    permissions = session.get('permissions').split(',')
    # print(permissions,request.path.split('/')[-1])
    try:
        print(request.path.split('/')[-1])
        if 'all' in permissions:return True
        elif (request.path.split('/')[-1] in permissions) or (perm[request.path.split('/')[-1]] in permissions):return True
        else: return False
    except KeyError:return False

#################################################


# Decorators ####################################

# User must logged in
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# User must logged out
def logout_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_not_authenticated():
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapper

# User must have permission
def permissions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not have_permissions():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

#################################################
