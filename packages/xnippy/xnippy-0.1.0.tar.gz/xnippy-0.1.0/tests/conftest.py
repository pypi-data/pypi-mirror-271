import pytest
from xnippy import Manager, __version__

@pytest.fixture
def config():
    mng = Manager('xnippy', __version__, )
    
    return 
