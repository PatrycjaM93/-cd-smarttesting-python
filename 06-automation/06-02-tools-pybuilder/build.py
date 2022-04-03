#   -*- coding: utf-8 -*-
from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")


name = "smarttesting_pyb_demo"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("dir_source_main_python", "smarttesting_pyb_demo")
    project.set_property("dir_source_unittest_python", "smarttesting_pyb_demo/tests")
    project.set_property("dir_source_main_scripts", "scripts")
