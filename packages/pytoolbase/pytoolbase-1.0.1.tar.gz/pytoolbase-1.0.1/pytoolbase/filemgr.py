##
##

import os
from typing import Union
from pathlib import Path
from pytoolbase.synchronize import synchronize


class FileManager(object):

    def __init__(self, root_dir: Union[str, None] = None):
        self.root_dir = root_dir if root_dir is not None else Path.home()

    @synchronize()
    def make_dir(self, *args):
        rel_path = os.path.join(*args)
        if not Path(str(rel_path)).is_absolute():
            full_path = os.path.join(self.root_dir, str(rel_path))
        else:
            full_path = rel_path
        path_dir = os.path.dirname(full_path)
        if not os.path.exists(path_dir):
            self.make_dir(path_dir)
        else:
            os.mkdir(full_path)
