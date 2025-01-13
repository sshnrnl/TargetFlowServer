from flask import Flask, render_template, request, redirect, url_for
from os.path import dirname, basename, isfile, join
import glob
from hori import *

route = glob.glob(join(dirname(__file__) ,"*.py"))
__all__ = [ basename(f)[:-3] for f in route if isfile(f) and not f.endswith('__init__.py')]
for j in __all__:
    __import__(f'routing.'+j)