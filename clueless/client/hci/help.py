import os
import webbrowser

import clueless
base_dir = os.path.dirname(clueless.__file__)
help_file = "file:///{base_dir}/help/clueless_help.htm".format(
    base_dir=base_dir)

def open():
    webbrowser.open(help_file)
