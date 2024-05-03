import os

if os.environ.get('INSIDE_KFP_FUNC_CONTAINER'):
    def run(**kwargs):
        if 'func' in kwargs:
            kwargs['func']()
else:
    from .task import *