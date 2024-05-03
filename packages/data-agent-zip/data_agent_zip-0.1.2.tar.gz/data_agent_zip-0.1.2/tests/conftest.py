"""
    Dummy conftest.py for data_agent_zip.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest

from data_agent_zip.connector import ZipConnector


@pytest.fixture
def zip_archive():
    conn = ZipConnector()
    conn.connect()

    # for grp in conn.list_groups():
    #     conn.unregister_group(grp)

    yield conn
    conn.disconnect()
