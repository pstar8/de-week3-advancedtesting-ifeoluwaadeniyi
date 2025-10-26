import pytest
import json
import os
import tempfile
from order_pipeline.pipeline import Pipeline


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_directory = tempfile.mkdtemp()
    yield temp_directory
    
    # Cleanup
    for file in os.listdir(temp_directory):
        os.remove(os.path.join(temp_directory, file))
    os.rmdir(temp_directory)


def test_pipeline_runs_successfully(temp_dir):
    """Test that pipeline runs without errors."""
    output_file = os.path.join(temp_dir, 'output.json')
    
    pipeline = Pipeline('../shoplink.json', output_file)
    results = pipeline.run()
    
    # Check results structure
    assert 'total_revenue' in results
    assert 'average_revenue' in results
    assert 'payment_status_counts' in results
    
    # Check output file was created
    assert os.path.exists(output_file)


def test_pipeline_produces_clean_data(temp_dir):
    """Test that pipeline produces correctly cleaned data."""
    output_file = os.path.join(temp_dir, 'output.json')
    
    pipeline = Pipeline('../shoplink.json', output_file)
    results = pipeline.run()
    
    # Read output file
    with open(output_file, 'r', encoding='utf-8') as f:
        clean_data = json.load(f)
    
    # Verify data is clean
    assert len(clean_data) > 0
    
    for order in clean_data:
        # Check all required fields exist
        assert 'order_id' in order
        assert 'quantity' in order
        assert 'price' in order
        assert 'total' in order
        assert 'payment_status' in order
        
        # Check types are correct
        assert isinstance(order['quantity'], int)
        assert isinstance(order['price'], float)
        assert isinstance(order['total'], float)
        
        # Check payment status is normalized
        assert order['payment_status'].islower()


def test_pipeline_analytics_correct(temp_dir):
    """Test that pipeline produces correct analytics."""
    output_file = os.path.join(temp_dir, 'output.json')
    
    pipeline = Pipeline('../shoplink.json', output_file)
    results = pipeline.run()
    
    # Read output to verify analytics
    with open(output_file, 'r', encoding='utf-8') as f:
        clean_data = json.load(f)
    
    # Verify total revenue
    expected_total = sum(order['total'] for order in clean_data)
    assert abs(results['total_revenue'] - expected_total) < 0.01
    
    # Verify average revenue
    expected_avg = expected_total / len(clean_data) if clean_data else 0
    assert abs(results['average_revenue'] - expected_avg) < 0.01
    
    # Verify counts add up
    total_count = sum(results['payment_status_counts'].values())
    assert total_count == len(clean_data)


def test_pipeline_integration():
    output_file = 'shoplink_cleaned.json'
    
    # Run pipeline
    pipeline = Pipeline('../shoplink.json', output_file)
    results = pipeline.run()
    
    print(f"\n📊 Pipeline Results:")
    print(f"   Total Revenue: ${results['total_revenue']:.2f}")
    print(f"   Average Revenue: ${results['average_revenue']:.2f}")
    print(f"   Payment Status Counts: {results['payment_status_counts']}")
    
    # Verify output file exists
    assert os.path.exists(output_file)
    
    # Verify it's valid JSON
    with open(output_file, 'r', encoding='utf-8') as f:
        clean_data = json.load(f)
    
    assert len(clean_data) > 0
    
    # Cleanup
    if os.path.exists(output_file):
        os.remove(output_file)