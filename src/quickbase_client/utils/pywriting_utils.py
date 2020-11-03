import abc
import os
from pathlib import Path
from typing import Dict
from typing import TextIO


class PyPackageWriter(object):

    def __init__(self, pkg_name, parent_dir=None):
        self.pkg_name = pkg_name
        self.parent_dir = os.getcwd() if parent_dir is None else parent_dir
        self.modules: Dict[str, PyFileWriter] = {}
        self.init_module = BasicPyFileWriter()
        self.add_module('__init__', self.init_module)

    @property
    def pkg_path(self):
        return os.path.join(self.parent_dir, self.pkg_name)

    def has_module_name(self, module_name):
        return module_name in self.modules

    def add_module(self, module_name, pyfile: 'PyFileWriter'):
        self.modules[module_name] = pyfile

    def write(self):
        for module_name, pyfile in self.modules.items():
            Path(self.pkg_path).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(self.pkg_path, f'{module_name}.py'), 'w') as f:
                pyfile.dump(f)


class PyFileWriter(abc.ABC):

    @abc.abstractmethod
    def get_file_as_string(self):
        pass

    def dump(self, dest: TextIO):
        dest.write(self.get_file_as_string())


class BasicPyFileWriter(PyFileWriter):
    """
    A simple class to help writing out python files. Could alternatively render jinja templates
    but this gives a little more potential flexibility and the general files we are trying
    to write are not complex enough to really need a jinja template. Plus this is just more fun.
    """

    # @attr.s(auto_attribs=True)
    # class Line:
    #     lineno: int
    #     s: str

    def __init__(self, indent='    '):
        super().__init__()
        self.indent = indent
        self.lines = []

    def add_line(self, s, level=0):
        self.lines.append(f'{self.indent * level}{s}')
        return self

    def space(self):
        return self.add_line('')

    def add_comment(self, comment, level=0):
        return self.add_line(f'# {comment}', level)

    def get_file_as_string(self):
        return '\n'.join(self.lines) + '\n'
