import time
import importlib


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
    module = importlib.import_module("protocol." + ".".join(components) + "_pb2")
    return getattr(module, components[-1])
