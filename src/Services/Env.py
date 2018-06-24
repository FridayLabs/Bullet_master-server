import io
import os
import re
import sys
import codecs
import warnings
import fileinput
from collections import OrderedDict
from subprocess import Popen, PIPE, STDOUT


class Env:
    __posix_variable = re.compile('\$\{[^\}]*\}')
    __escape_decoder = codecs.getdecoder('unicode_escape')

    def __init__(self, dotenv_path):
        self.dotenv_path = dotenv_path
        self.__dict = None

    def dict(self):
        if self.__dict:
            return self.__dict

        values = OrderedDict(self.__parse())
        self.__dict = self.__resolve_nested_variables(values)
        return self.__dict

    def __get_stream(self):
        self._is_file = False
        if isinstance(self.dotenv_path, io.StringIO):
            return self.dotenv_path

        if os.path.exists(self.dotenv_path):
            self._is_file = True
            return io.open(self.dotenv_path)

        return io.StringIO('')

    def __parse(self):
        f = self.__get_stream()

        for line in f:
            key, value = self.__parse_line(line)
            if not key:
                continue

            yield key, value

        if self._is_file:
            f.close()

    def set_as_environment_variables(self):
        for k, v in self.dict().items():
            if k not in os.environ:
                os.environ[k] = v

    def __parse_line(self, line):
        line = line.strip()

        if not line or line.startswith('#') or '=' not in line:
            return None, None

        k, v = line.split('=', 1)

        if k.startswith('export '):
            k = k.lstrip('export ')

        k, v = k.strip(), v.strip()

        if v:
            v = v.encode('unicode-escape').decode('ascii')
            quoted = v[0] == v[-1] in ['"', "'"]
            if quoted:
                v = self.__decode_escaped(v[1:-1])

        return k, v

    def __decode_escaped(self, escaped):
        return self.__escape_decoder(escaped)[0]

    def __resolve_nested_variables(self, values):
        def __replacement(name):
            ret = os.getenv(name, values.get(name, ""))
            return ret

        def __re_sub_callback(match_object):
            return __replacement(match_object.group()[2:-1])

        for k, v in values.items():
            values[k] = self.__posix_variable.sub(__re_sub_callback, v)

        return values
