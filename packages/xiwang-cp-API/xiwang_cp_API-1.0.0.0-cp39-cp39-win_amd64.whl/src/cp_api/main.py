# -*- coding: utf-8 -*-
from bin.core import base
from flask import Blueprint
from API import api
import os


class MainClass(api):
    IsFlaskMode = True
    name = 'api'

    def __init__(self):
        super().__init__()

    @staticmethod
    def read_module(required):
        api_dir = os.path.dirname(os.path.abspath(__file__))
        bp_path = os.path.join(api_dir, 'View')
        bpfs = os.listdir(bp_path)
        bps = []
        for bpf in bpfs:
            try:
                pth = os.path.join(bp_path, bpf)
                if bpf != '__init__.py' and os.path.isfile(pth):
                    name = bpf.split('.')[0]
                    bp = Blueprint(name=name, import_name=name, url_prefix='/%s' % name)
                    co = base.load_class('View', bp_path, bpf, 'View')
                    func = list(filter(lambda x: not x.startswith('__') and not x.endswith('__'), dir(co)))
                    for f in func:
                        fun = getattr(co, f)
                        arg_str = ''
                        if fun.__code__.co_argcount > 0:
                            for i in range(fun.__code__.co_argcount):
                                arg = fun.__code__.co_varnames[i]
                                if arg != 'self':
                                    arg_str += '/<' + arg + '>'
                        bp.add_url_rule(rule='/' + (f if f != 'index' else '') + arg_str, endpoint=f, view_func=fun,
                                        methods=['GET', 'POST'])
                        # required(
                    bps.append(bp)
            except Exception as ex:
                base.log('error', str(ex))
        return bps
