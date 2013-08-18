import os
import webbrowser

import clueless
base_dir = os.path.dirname(clueless.__file__)
help_file = "file:///etc/clueless/clueless_help.htm"

def open():
    webbrowser.open(help_file)
