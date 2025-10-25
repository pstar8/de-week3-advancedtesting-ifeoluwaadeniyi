import pytest
import os
import tempfile
from order_pipeline.reader import Reader

@pytest.fixture
def temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir

    # Cleanup
    files = os.listdir(temp_dir)
    for file in files:
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

def test_temp_dir_works(temp_dir):
    assert isinstance(temp_dir, str)
    
    # Check that the directory exists
    assert os.path.exists(temp_dir)

    # Check that it's indeed a directory
    assert os.path.isdir(temp_dir)

# def test_with_real_data():
#     reader = Reader('../order_pipeline/shoplink.json')
#     data = reader.read()
#     assert len(data) == 10

    print(f"\n✅ Temp directory created: {temp_dir}")