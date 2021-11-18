# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 14:47:48 2016

@author: lviton

based on:
    http://stackoverflow.com/questions/2312210/window-icon-of-exe-in-pyqt4
    https://packaging.python.org/distributing/#setup-py
    https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages
import py2exe

setup(name='SystemMeasure',
      version='1.0',
      description='System to measure characteristics of sensors',
      author='Luighi Anthony Viton Zorrilla',
      author_email='luighiavz@gmail.com',
      url='',
      packages=['systemmeasure'],
      windows=[{"script":"systemmeasure/applicationmodule.py",
                "icon_resources":[(1, "images/measuresys.ico")]}], 
      data_files = [
            ('imageformats', [
              r'C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll'
              ])],
      options={"py2exe":{"packages":["gzip"],
                         "includes":["sip"],
                            "dll_excludes":["MSVCP90.dll"]}})