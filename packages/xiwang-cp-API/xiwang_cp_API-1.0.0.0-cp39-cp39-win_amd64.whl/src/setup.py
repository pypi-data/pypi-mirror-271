# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def c_compile(name: str, modules):
    module_list = []
    for m in modules:
        module_list.append(
            Extension(name=m[0], sources=[m[1]])
        )
    setup(name="xiwang_cp_API", python_requires='>=3',
          version="1.0.0.0", keywords="pack, api",
          install_requires=['flask'],
          ext_modules=cythonize(module_list=module_list, language_level="3"),
          description="flask的API插件",
          long_description=readme(), long_description_content_type='text/markdown',
          author="xiwang", author_email="xiwang0439@hotmail.com",
          url="https://www.xi-wang.cn",
          download_url="https://www.xi-wang.cn/download/",
          package_data={
              "": ["./*.yaml"],
          },
          packages=find_packages(),
          classifiers=["Programming Language :: Python :: 3",
                       "License :: OSI Approved :: MIT License",
                       "Operating System :: OS Independent",],
          )


c_compile(name="cp_API", modules=[("main", "src/cp_api/main.py"),
                                  ("API", "src/cp_api/API.py"),
                                  # ("setup", "setup.py"),
                                  ("View.__init__", "src/cp_api/View/__init__.py"),
                                  ("View.file", "src/cp_api/View/file.py"),
                                  ("View.scheduler", "src/cp_api/View/scheduler.py"),
                                  ])
