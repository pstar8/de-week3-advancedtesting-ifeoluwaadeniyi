import pytest
import json
import os
import tempfile
from order_pipeline.exporter import Exporter

@pytest.fixture
def temp_dir():
    temp_directory = tempfile.mkdtemp()
    yield temp_directory
    
    for file in os.listdir(temp_directory):
        os.remove(os.path.join(temp_directory, file))
    os.rmdir(temp_directory)


# Testing shoplink

def test_export_transformed_shoplink_data(temp_dir):

    from order_pipeline.reader import Reader
    from order_pipeline.validator import Validator
    from order_pipeline.transformer import Transformer
    
    reader = Reader('../shoplink.json')
    raw_data = reader.read()
    
    validator = Validator()
    valid_data = validator.validate(raw_data)
    
    transformer = Transformer()
    transformed_data = transformer.transform(valid_data)
    
    # Export
    filepath = os.path.join(temp_dir, 'shoplink_cleaned.json')
    exporter = Exporter(filepath)
    exporter.export(transformed_data)
    
    print(f"\n✅ Exported {len(transformed_data)} cleaned orders to {filepath}")
    
    # Verify file exists
    assert os.path.exists(filepath)
    
    # Read back and verify
    with open(filepath, 'r', encoding='utf-8') as f:
        exported_data = json.load(f)
    
    assert len(exported_data) == len(transformed_data)
