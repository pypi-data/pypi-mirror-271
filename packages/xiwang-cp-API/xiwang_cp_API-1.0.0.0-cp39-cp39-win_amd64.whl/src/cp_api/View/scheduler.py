# -*- coding: utf-8 -*-
from flask import jsonify, abort
import os


class View:
    def get(self):
        print(os.getcwd())
        return jsonify({'asdfsd': 'dfdf'})
