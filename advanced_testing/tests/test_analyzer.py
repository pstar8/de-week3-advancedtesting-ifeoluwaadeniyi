import pytest
from order_pipeline.analyzer import Analyzer

def test_calculate_total_revenue_basic():
    analyzer = Analyzer()
    
    data = [
        {"order_id": "ORD001", "total": 31.98, "payment_status": "paid"},
        {"order_id": "ORD002", "total": 12.50, "payment_status": "paid"},
        {"order_id": "ORD003", "total": 50.00, "payment_status": "pending"}
    ]
    
    result = analyzer.calculate_total_revenue(data)
    
    assert result == 94.48

# Tests for _calculate_average_revenue()

def test_calculate_average_revenue_basic():
    analyzer = Analyzer()
    
    data = [
        {"order_id": "ORD001", "total": 30.00, "payment_status": "paid"},
        {"order_id": "ORD002", "total": 60.00, "payment_status": "paid"},
        {"order_id": "ORD003", "total": 90.00, "payment_status": "pending"}
    ]
    
    result = analyzer.calculate_average_revenue(data)
    
    assert result == 60.00

# Tests for _count_payment_statuses()

def test_count_payment_statuses_basic():
    """Test basic payment status counting."""
    analyzer = Analyzer()
    
    data = [
        {"order_id": "ORD001", "total": 30.00, "payment_status": "paid"},
        {"order_id": "ORD002", "total": 40.00, "payment_status": "paid"},
        {"order_id": "ORD003", "total": 50.00, "payment_status": "pending"},
        {"order_id": "ORD004", "total": 60.00, "payment_status": "paid"},
        {"order_id": "ORD005", "total": 70.00, "payment_status": "refunded"}
    ]
    
    result = analyzer.count_payment_statuses(data)
    
    assert result["paid"] == 3
    assert result["pending"] == 1
    assert result["refunded"] == 1


def test_analyze_complete_analysis():
    """Test complete analysis with multiple orders."""
    analyzer = Analyzer()
    
    data = [
        {"order_id": "ORD001", "total": 31.98, "payment_status": "paid"},
        {"order_id": "ORD002", "total": 12.50, "payment_status": "paid"},
        {"order_id": "ORD003", "total": 50.00, "payment_status": "pending"}
    ]
    
    result = analyzer.analyze(data)
    
    # Check structure
    assert "total_revenue" in result
    assert "average_revenue" in result
    assert "payment_status_counts" in result
    
    # Check values
    assert result["total_revenue"] == 94.48
    assert round(result["average_revenue"], 2) == 31.49
    assert result["payment_status_counts"]["paid"] == 2
    assert result["payment_status_counts"]["pending"] == 1