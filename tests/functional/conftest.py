import os
import inject
import pytest
from src.Services.Configurator import Configurator


@pytest.fixture()
def migrations():
    migrator = inject.instance('Migrator')
    migrator.migrate()
    yield
    migrator.rollback()
