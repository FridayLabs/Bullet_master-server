import os
import pytest
import tempfile
import warnings
from src.Services.Env import Env


@pytest.mark.parametrize("test_input,expected", [
    ("a=b", ("a", "b")),
    (" a = b ", ("a", "b")),
    ("export a=b", ("a", "b")),
    (" export 'a'=b", ("'a'", "b")),
    (" export 'a'=b", ("'a'", "b")),
    ("# a=b", (None, None)),
    ("#a=b", (None, None)),
    ("a=b space ", ('a', 'b space')),
    ("a='b space '", ('a', 'b space ')),
    ('a="b space "', ('a', 'b space ')),
])
def test_parse_line(test_input, expected):
    dotenv_path = '/tmp/.test_load_dotenv'
    with open(dotenv_path, 'w') as f:
        f.write(test_input)
        f.close()
        env = Env(dotenv_path)
        assert env.parse_line(test_input) == expected


def test_warns_if_file_does_not_exist():
    with warnings.catch_warnings(record=True) as w:
        env = Env('.does_not_exist')
        assert len(w) == 1
        assert w[0].category is UserWarning
        assert str(w[0].message) == "File doesn't exist .does_not_exist"


def test_load_dotenv():
    dotenv_path = '/tmp/.test_load_dotenv'
    with open(dotenv_path, 'w') as f:
        f.write('KEK=LOL')
        f.close()
        env = Env(dotenv_path)
        env.set_as_environment_variables()
        assert 'KEK' in os.environ
        assert os.environ['KEK'] == 'LOL'


def test_load_dotenv_not_override():
    dotenv_path = '/tmp/.test_load_dotenv_override'
    key_name = "DOTENV_OVER"
    os.environ[key_name] = "KEK"
    with open(dotenv_path, 'w') as f:
        f.write(key_name + '=LOL')
        f.close()
        env = Env(dotenv_path)
        env.set_as_environment_variables()
        assert os.environ[key_name] == 'KEK'


def test_load_dotenv_resolve():
    dotenv_path = '/tmp/.test_load_dotenv_resolve'
    with open(dotenv_path, 'w') as f:
        f.write(u"BAR=BAZ\nFOO=${BAR}")
        f.close()
        env = Env(dotenv_path)
        env.set_as_environment_variables()
        assert 'BAR' in os.environ
        assert 'FOO' in os.environ
        assert os.environ['FOO'] == 'BAZ'


def test_load_dotenv_decode():
    dotenv_path = '/tmp/.test_load_dotenv_decode'
    with open(dotenv_path, 'w') as f:
        f.write(u"BAR2='BAZ2'\nLAL=\"WUT\"\n\"WUT\"=LAL")
        f.close()
        env = Env(dotenv_path)
        env.set_as_environment_variables()
        assert 'BAR2' in os.environ
        assert 'LAL' in os.environ
        assert '"WUT"' in os.environ
        assert os.environ['BAR2'] == "BAZ2"
        assert os.environ['LAL'] == 'WUT'
        assert os.environ['"WUT"'] == 'LAL'


def test_dotenv_unicode():
    dotenv_path = '/tmp/.test_load_dotenv_unicode'
    with open(dotenv_path, 'w') as f:
        f.write(u'hello="it works!😃"\nDOTENV=${hello}\n')
        f.close()
        env = Env(dotenv_path)
        env.set_as_environment_variables()
        assert 'DOTENV' in os.environ
        assert os.environ['DOTENV'] == u'it works!😃'
