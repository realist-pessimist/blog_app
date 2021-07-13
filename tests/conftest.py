import os
import tempfile

import pytest

from blog.models import Article


@pytest.fixture(autouse=True)
def database():
    fd, file_name = tempfile.mkstemp()
    os.environ['DATABASE_NAME'] = file_name
    Article.create_table(database_name=file_name)
    yield
    os.close(fd)
    os.unlink(file_name)
