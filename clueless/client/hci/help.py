import os
import webbrowser

import clueless.client.hci
base_dir = os.path.dirname(clueless.client.hci.__file__)
help_file = "file:///{base_dir}/resources/help/clueless_help.htm".format(
    base_dir=base_dir)

def open():
    webbrowser.open(help_file)
