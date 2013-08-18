import os
import webbrowser

import clueless
base_dir = os.path.dirname(clueless.__file__)
help_file = "file:///etc/clueless/clueless_help.htm"
webbrowser.open(help_file)

def open():
    webbrowser.open(help_file)
