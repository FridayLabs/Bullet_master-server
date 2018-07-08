import time
import importlib
import os
import pdb


def periodically(fn, alive, timeout, step=0.5):
    current_timeout = 0
    while alive():
        time.sleep(step)
        current_timeout += step
        if current_timeout >= timeout:
            current_timeout = 0
            fn()


def import_procotol_class(name):
    components = name.split('.')[1:]
    module_name = "protocol." + ".".join(components) + "_pb2"
    if os.path.isfile(module_name.replace('.', '/') + '.py'):
        module = importlib.import_module(module_name)
    else:
        module = importlib.import_module("google." + ".".join(components).lower() + "_pb2")
    return getattr(module, components[-1])


def packet_is_a(cls, message):
    return message.DESCRIPTOR.name == cls.DESCRIPTOR.name
