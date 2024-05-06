# -*- coding: utf-8 -*-
import os
import shutil
import tarfile

from flask import jsonify, request, render_template, redirect, current_app

UNZIP_FOLDER = os.path.join(os.getcwd(), 'uploads')
PLUGIN_FOLDER = os.path.join(os.getcwd(), 'plugin')
TEMP_FOLDER = os.path.join(os.getcwd(), 'temp')


def allowed_file(t, filename):
    extensions = ''
    if t == 'plugin':
        extensions = '.tar.gz'
    elif t == 'api_module':
        extensions = '.py'
    return filename.endswith(extensions) if extensions != '' else False


def unzip_plugin(t, filename):
    """
    指定文件解压到插件目录
    :param t:
    :type t:
    :param filename: 指定压缩文件
    :type filename: str
    :return: 返回成功（True）或报错
    :rtype: bool | Exception
    """
    try:
        with tarfile.open(get_path(t, filename), 'r') as tar_ref:
            tar_ref.extractall(PLUGIN_FOLDER)
        os.remove(get_path(t, filename))
        return True
    except Exception as ex:
        raise ex


def get_path(t, filename=None):
    if t != 'plugin':
        p = 'temp'
    elif filename:
        p = 'plugin'
    else:
        p = 'uploads'
    folder = os.path.join(os.getcwd(), p)
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder if filename is None else os.path.join(folder, filename)


class View:
    @staticmethod
    def index(t: str):
        if request.method == 'GET':
            if t == 'plugin':
                folder: list[str] = os.listdir(PLUGIN_FOLDER)
                mods: dict = {}
                return render_template('upload.html', plugin_list=folder)
            elif t == 'api_module':
                keys = current_app.blueprints.keys()
                m = [n for n in list(keys) if n.find('.') == -1]
                folder: list[str] = os.listdir(TEMP_FOLDER)
                return render_template('upload.html', temp_list=folder, plugin_list=m)

    @staticmethod
    def upload():
        if request.method == 'POST':
            file = request.files.get('formFile')
            t = request.form.get('type')
            if file and allowed_file(t, file.filename):
                file.save(get_path(t, file.filename))
                if t == 'plugin':
                    unzip_plugin(t, file.filename)
                elif t == 'api_module':
                    pass
            return jsonify({'state': 'ok'})

    @staticmethod
    def remove(t, o):
        if request.method == 'GET':
            path = get_path(t, o)
            print(path)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return jsonify({'state': 'ok'})

    @staticmethod
    def approve(t, o, module=None):
        pass
