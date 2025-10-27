import pytest
import os
import tempfile
from order_pipeline.validator import Validator
from order_pipeline.reader import Reader
    


def test_has_required_fields():
    validator = Validator()
    
    order_with_all_fields = {
        "order_id": "ORD007",
        "timestamp": "2025-10-19T08:30:00Z",
        "item": "Power Bank",
        "quantity": "N/A",
        "price": "$25",
        "total": "$50",
        "payment_status": "Paid"
    }

    result = validator.has_required_fields(order_with_all_fields)
    assert result is True

def test_missing_required_fields():
    validator = Validator()
    
    order_missing_fields = {
        "order_id": "ORD009",
        "timestamp": "2025-10-19T08:40:00Z",
        "item": "Webcam",
        "quantity": 1,
        "price": "$29.99",
        "payment_status": "PAID"
    }

    result = validator.has_required_fields(order_missing_fields)
    assert result is False

def test_validator_rejects_negative_quantity():
    validator = Validator()
    
    order = {
        "order_id": "ORD003",
        "timestamp": "2025-10-19T08:10:00Z",
        "item": "USB Cable",
        "quantity": -3,  # Negative number! 
        "price": "5usd",
        "payment_status": "pending",
        "total": 15
    }
    
    result = validator.numeric_fields_are_positive(order)
    assert result == False

def test_validator_rejects_zero_quantity():
    validator = Validator()
    
    order = {
        "order_id": "ORD999",
        "timestamp": "2025-10-19T08:00:00Z",
        "item": "Mouse",
        "quantity": 0,  # Zero! 
        "price": 15.99,
        "payment_status": "paid",
        "total": 0      #Zero!
    }
    
    result = validator.numeric_fields_are_positive(order)
    assert result == False

def test_validator_accepts_string_price():
    validator = Validator()
    
    order = {
        "order_id": "ORD001",
        "timestamp": "2025-10-19T08:00:00Z",
        "item": "Mouse",
        "quantity": 2,
        "price": "$15.99",  # String ✅
        "payment_status": "paid",
        "total": "$31.98"   # String ✅
    }
    
    result = validator.numeric_fields_are_parseable(order)
    assert result == True  

def test_is_a_valid_order():
    validator = Validator()
    order = {
        "order_id": "ORD005",
        "timestamp": "2025-10-19T08:20:00Z",
        "item": "Keyboard",
        "quantity": 1,
        "price": 45.00,
        "total": 45.00,
        "payment_status": "Paid"
    }
    
    result = validator.is_valid_order(order)
    assert result is True

    def test_validator_rejects_non_parseable_quantities():
        """Test that Validator rejects quantities like 'N/A'."""
        validator = Validator()
        
        order_with_na = {
            "order_id": "ORD007",
            "timestamp": "2025-10-19T08:30:00Z",
            "item": "Power Bank",
            "quantity": "N/A",  # ❌ Should be rejected!
            "price": "$25",
            "payment_status": "Paid",
            "total": "$50"
        }
        
        result = validator.is_valid_order(order_with_na)
        assert result == False
        
        # Test with valid parseable quantity
        order_with_parseable = {
            "order_id": "ORD004",
            "timestamp": "2025-10-19T08:15:00Z",
            "item": "Mouse",
            "quantity": "2pcs",  # ✅ Should be accepted (has digit '2')
            "price": "$16",
            "payment_status": "paid",
            "total": "$32.00"
        }
    
        result = validator.is_valid_order(order_with_parseable)
        assert result == True